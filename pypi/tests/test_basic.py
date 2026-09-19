"""Plain unittest, no third-party test runner."""

import unittest

import kaomoji_dataset as kd


class TestDataset(unittest.TestCase):
    def test_all_matches_stats(self):
        self.assertEqual(len(kd.all()), kd.stats["total"])

    def test_entry_shape(self):
        for e in kd.all()[:200]:
            self.assertIsInstance(e["id"], str)
            self.assertTrue(e["text"])
            self.assertIsInstance(e["emotion"], list)
            self.assertIn(e["tier"], ("core", "extended", "mixed", "verbose"))

    def test_ids_unique(self):
        self.assertEqual(len({e["id"] for e in kd.all()}), kd.stats["total"])

    def test_search_is_cross_lingual(self):
        en = [e["id"] for e in kd.search("happy", limit=3)]
        self.assertTrue(en)
        for q in ("嬉しい", "开心", "feliz"):
            self.assertEqual([e["id"] for e in kd.search(q, limit=3)], en, q)

    def test_search_honours_limit(self):
        self.assertEqual(len(kd.search("happy", limit=3)), 3)

    def test_search_defaults_to_50(self):
        self.assertEqual(len(kd.search("happy")), 50)

    def test_negative_limit_means_no_limit(self):
        """It used to fall through to items[:-1] — a wrong answer that looks right."""
        every = kd.search("happy", limit=-1)
        self.assertGreater(len(every), 50)
        expected = [
            e for e in kd.all()
            if any(
                "happy" in (e["names"].get(l) or "").lower()
                or any("happy" in str(w).lower() for w in (e["keywords"].get(l) or []))
                for l in kd.LANGS
            )
        ]
        self.assertEqual(len(every), len(expected))
        self.assertEqual(len(kd.by_category("happy", limit=-1)), len(kd.by_category("happy")))
        self.assertEqual(len(kd.search("happy", limit=0)), 0)

    def test_search_of_nonsense(self):
        self.assertEqual(kd.search("zzzzqqqqxxxx"), [])

    def test_by_category(self):
        top = kd.categories()[0]
        self.assertEqual(len(kd.by_category(top["name"])), top["count"])

    def test_by_emotion(self):
        self.assertTrue(kd.by_emotion("happy", limit=10))

    def test_random_respects_filter(self):
        for _ in range(50):
            self.assertEqual(kd.random(tier="core")["tier"], "core")

    def test_random_empty_pool(self):
        self.assertIsNone(kd.random(category="no-such-category"))

    def test_originals(self):
        self.assertEqual(len(kd.originals()), kd.stats["originals"])

    def test_tier_totals(self):
        counts = {}
        for e in kd.all():
            counts[e["tier"]] = counts.get(e["tier"], 0) + 1
        self.assertEqual(counts, kd.stats["tiers"])


if __name__ == "__main__":
    unittest.main()
