import unittest

from rx_shortage_radar.rxnorm import parse_approximate_candidates


class RxNormTests(unittest.TestCase):
    def test_parse_approximate_candidates_deduplicates_rxcui(self):
        payload = {
            "approximateGroup": {
                "candidate": [
                    {"rxcui": "142153", "name": "Albuterol Sulfate", "score": "10.9", "rank": "1", "source": "RXNORM"},
                    {"rxcui": "142153", "name": "ALBUTEROL SULFATE", "score": "10.9", "rank": "1", "source": "USP"},
                    {"rxcui": "123", "name": "Other", "score": "1.5", "rank": "2", "source": "RXNORM"},
                ]
            }
        }
        candidates = parse_approximate_candidates(payload)
        self.assertEqual([candidate.rxcui for candidate in candidates], ["142153", "123"])
        self.assertEqual(candidates[0].name, "Albuterol Sulfate")


if __name__ == "__main__":
    unittest.main()

