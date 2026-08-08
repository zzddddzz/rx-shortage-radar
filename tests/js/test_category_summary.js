const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const { summarizeTherapeuticCategories } = require("../../site/category-summary.js");

const fixturePath = path.join(__dirname, "..", "fixtures", "multi_category_groups.json");
const groups = JSON.parse(fs.readFileSync(fixturePath, "utf8"));

test("counts a multi-category group once in every listed category", () => {
  const summary = summarizeTherapeuticCategories(groups);

  assert.equal(summary.groupCount, 4);
  assert.equal(summary.missingCategoryGroups, 2);
  assert.deepEqual(summary.categories, [
    { name: "Pediatric", count: 2 },
    { name: "Pulmonary/Allergy", count: 1 },
  ]);
  assert.notEqual(
    summary.categories.reduce((total, category) => total + category.count, 0),
    summary.groupCount,
    "category assignments are non-additive and must not be treated as the matching group total",
  );
});

test("reports a clear all-missing category state", () => {
  const summary = summarizeTherapeuticCategories([
    { id: "missing-a", therapeutic_categories: [] },
    { id: "missing-b" },
  ]);

  assert.deepEqual(summary.categories, []);
  assert.equal(summary.groupCount, 2);
  assert.equal(summary.missingCategoryGroups, 2);
});
