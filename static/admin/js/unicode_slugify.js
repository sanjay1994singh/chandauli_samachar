(function () {
  "use strict";

  function unicodeSlugify(value) {
    return value
      .normalize("NFKC")
      .toLocaleLowerCase()
      .replace(/[^\p{L}\p{N}\p{M}\s_-]/gu, "")
      .trim()
      .replace(/[\s_-]+/g, "-")
      .replace(/-+/g, "-")
      .replace(/^-|-$/g, "");
  }

  function initializeUnicodeSlugs() {
    const configElement = document.getElementById("django-admin-prepopulated-fields-constants");
    if (!configElement) return;

    let configurations;
    try {
      configurations = JSON.parse(configElement.dataset.prepopulatedFields || "[]");
    } catch (error) {
      return;
    }

    configurations.forEach((configuration) => {
      const slugInput = document.querySelector(configuration.id);
      const sourceInput = document.querySelector(configuration.dependency_ids[0]);
      if (!slugInput || !sourceInput) return;

      let manuallyEdited = Boolean(slugInput.value);

      slugInput.addEventListener("input", (event) => {
        if (event.isTrusted) manuallyEdited = Boolean(slugInput.value);
      });

      sourceInput.addEventListener("input", () => {
        if (manuallyEdited) return;
        // Run after Django's built-in URLify listener so Hindi matras are preserved.
        window.setTimeout(() => {
          slugInput.value = unicodeSlugify(sourceInput.value).slice(0, configuration.maxLength || 50);
          slugInput.dispatchEvent(new Event("change", { bubbles: true }));
        }, 0);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeUnicodeSlugs);
  } else {
    initializeUnicodeSlugs();
  }
})();
