import http.server
import json
import urllib.parse
import importlib
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.failure_analyzer import analyze_response, analyze_conversation
from taxonomy.taxonomy_utils import load_taxonomy
from analysis.risk_analysis import generate_risk_report

class APIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/api/taxonomy":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(load_taxonomy()).encode("utf-8"))
        elif path == "/api/risk-report":
            demo_failures = {
                "hallucinations": 15,
                "context_loss": 7,
                "fake_confidence": 11,
                "instruction_drift": 6,
                "manipulation": 2,
                "recursive_reasoning_collapse": 3,
            }
            # Generate the report dict (which also writes to disk)
            report = generate_risk_report(demo_failures)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(report).encode("utf-8"))
        elif path == "/api/run-evals":
            TEST_MODULES = [
                "experiments.reproducible_evals.test_hallucination_citation",
                "experiments.reproducible_evals.test_fake_confidence",
                "experiments.reproducible_evals.test_context_loss",
                "experiments.reproducible_evals.test_instruction_drift",
                "experiments.reproducible_evals.test_manipulation",
                "experiments.reproducible_evals.test_recursive_collapse",
            ]
            results = []
            for module_name in TEST_MODULES:
                short_name = module_name.rsplit(".", 1)[-1]
                try:
                    mod = importlib.import_module(module_name)
                    importlib.reload(mod)
                    
                    if short_name == "test_context_loss":
                        turns, expected = mod.create_conversation_test()
                        analyses = analyze_conversation(turns)
                        last_analysis = analyses[-1] if analyses else {}
                        passed = last_analysis.get("detected_failure") == expected["failure_type"]
                        results.append({
                            "name": short_name,
                            "passed": passed,
                            "prompt": "Multi-turn conversation history...",
                            "response": turns[-1]["content"],
                            "expected_failure": expected["failure_type"],
                            "detected_failure": last_analysis.get("detected_failure"),
                            "detected_subtype": last_analysis.get("detected_subtype"),
                            "confidence": last_analysis.get("confidence", 0.0),
                            "evidence": last_analysis.get("evidence", [])
                        })
                    else:
                        prompt, expected = mod.create_test_case()
                        sim_response = getattr(mod, "SIMULATED_LLM_RESPONSE", "")
                        analysis = analyze_response(sim_response, prompt, expected_failure=expected["failure_type"])
                        passed = analysis["detected_failure"] == expected["failure_type"]
                        results.append({
                            "name": short_name,
                            "passed": passed,
                            "prompt": prompt,
                            "response": sim_response,
                            "expected_failure": expected["failure_type"],
                            "detected_failure": analysis["detected_failure"],
                            "detected_subtype": analysis["detected_subtype"],
                            "confidence": analysis["confidence"],
                            "evidence": analysis["evidence"]
                        })
                except Exception as exc:
                    results.append({
                        "name": short_name,
                        "passed": False,
                        "error": str(exc)
                    })
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(results).encode("utf-8"))
        else:
            # Default fallback to serve static files (index.html, etc.)
            super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/api/analyze":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode("utf-8"))
                prompt = data.get("prompt", "")
                response = data.get("response", "")
                
                result = analyze_response(response, prompt)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8000):
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, APIHandler)
    print(f"Starting server on port {port}...")
    print(f"Open http://localhost:{port} in your browser to view the dashboard.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI Failure Observatory Local Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()
    run_server(args.port)
