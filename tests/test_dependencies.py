"""Exercise real dependency callers against a local synthetic product page.

These tests do not scrape retailers or claim the prototype calculator is complete.
"""
import contextlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
import unittest
from unittest.mock import patch

import server


class ProductPage(BaseHTTPRequestHandler):
    headers_seen = []

    def do_GET(self):
        type(self).headers_seen.append(dict(self.headers))
        body = b"<html><h1>Nike shirt</h1><p>Synthetic garment fixture</p></html>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


@contextlib.contextmanager
def product_page():
    with ThreadingHTTPServer(("127.0.0.1", 0), ProductPage) as http:
        worker = threading.Thread(target=http.serve_forever, daemon=True)
        worker.start()
        try:
            yield "http://127.0.0.1:" + str(http.server_port) + "/product"
        finally:
            http.shutdown()
            worker.join(timeout=2)


class DependencyContracts(unittest.TestCase):
    def setUp(self):
        server.app.config.update(TESTING=True)
        self.client = server.app.test_client()
        ProductPage.headers_seen.clear()

    def test_home_and_default_cors_remain_compatible(self):
        response = self.client.get("/", headers={"Origin": "https://extension.example"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Hello World!")
        self.assertEqual(response.headers["Access-Control-Allow-Origin"], "https://extension.example")
        self.assertNotIn("Access-Control-Allow-Credentials", response.headers)

    def test_real_requests_bs4_and_useragent_scrape_product(self):
        with product_page() as url:
            data = server.scrape.start_scrape(url)
        self.assertEqual(data, ["shirt", "Nike", ["Cotton: 80%", "Polyester: 20%"], -1, 1])
        self.assertEqual(len(ProductPage.headers_seen), 1)
        self.assertIn("Chrome/108.0.0.0", ProductPage.headers_seen[0]["User-Agent"])

    def test_webscrape_route_preserves_the_real_http_json_contract(self):
        with product_page() as url:
            response = self.client.get("/webscrape", query_string={"url": url})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "cloth_type": "shirt", "brand": "Nike",
            "materials": ["Cotton: 80%", "Polyester: 20%"],
            "num_washes": -1, "weight_grams": 1,
        })
        self.assertEqual(response.headers["Access-Control-Allow-Origin"], "*")
        self.assertNotIn("Access-Control-Allow-Credentials", response.headers)

    def test_missing_url_preserves_the_existing_error_response(self):
        response = self.client.get("/webscrape")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Error processing, are you sure this is a valid url?")

    def test_submit_forwards_fields_and_serializes_calculator_values(self):
        fields = {"brand": "Nike", "cloth_type": "shirt", "materialone": "Cotton: 80%",
                  "materialtwo": "Polyester: 20%", "num_washes": "125", "weight": "800"}
        with patch.object(server.calc, "start_calc", return_value=[85, 70, 125]) as calc:
            response = self.client.get("/submit", query_string=fields)
        calc.assert_called_once_with("Nike", "shirt", "Cotton: 80%", "Polyester: 20%", "125", "800")
        self.assertEqual(response.get_json(), {"sustainability_rating": 85, "fabric_quality": 70, "num_washes": 125})

    def test_existing_calculator_placeholder_is_not_changed_by_dependency_work(self):
        self.assertEqual(server.calc.start_calc("Nike", "shirt", "Cotton: 80%", "Polyester: 20%", "125", "800"), "hello world")

    def test_preflight_preserves_methods_headers_and_no_credentials(self):
        response = self.client.options("/webscrape", headers={
            "Origin": "https://extension.example", "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("GET", response.headers["Access-Control-Allow-Methods"])
        self.assertEqual(response.headers["Access-Control-Allow-Origin"], "https://extension.example")
        self.assertIn("content-type", response.headers["Access-Control-Allow-Headers"].lower())
        self.assertNotIn("Access-Control-Allow-Credentials", response.headers)


if __name__ == "__main__":
    unittest.main()
