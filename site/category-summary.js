(function attachCategorySummary(globalScope) {
  "use strict";

  function summarizeTherapeuticCategories(records) {
    const groups = Array.isArray(records) ? records : [];
    const categoryCounts = new Map();
    let missingCategoryGroups = 0;

    for (const group of groups) {
      const categories = new Set(
        (Array.isArray(group.therapeutic_categories) ? group.therapeutic_categories : [])
          .map((category) => String(category || "").trim())
          .filter(Boolean),
      );

      if (!categories.size) {
        missingCategoryGroups += 1;
        continue;
      }

      for (const category of categories) {
        categoryCounts.set(category, (categoryCounts.get(category) || 0) + 1);
      }
    }

    const categories = Array.from(categoryCounts, ([name, count]) => ({ name, count }));
    categories.sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));

    return {
      groupCount: groups.length,
      missingCategoryGroups,
      categories,
    };
  }

  const api = Object.freeze({ summarizeTherapeuticCategories });
  globalScope.CategorySummary = api;
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
})(typeof window === "object" ? window : globalThis);
