document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("storyForm");
  const generateBtn = document.getElementById("generateBtn");
  const btnText = generateBtn.querySelector(".btn-text");
  const loader = generateBtn.querySelector(".loader");
  const outputSection = document.getElementById("outputSection");
  const inputSection = document.querySelector(".input-section");
  const storyTitleDisplay = document.getElementById("storyTitleDisplay");
  const storyContent = document.getElementById("storyContent");
  const storySource = document.getElementById("storySource");
  const resetBtn = document.getElementById("resetBtn");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // UI Loading State
    generateBtn.disabled = true;
    btnText.textContent = "Generating Magic...";
    loader.style.display = "inline-block";

    const data = {
      title: document.getElementById("title").value,
      prompt: document.getElementById("prompt").value,
      characters: document.getElementById("characters").value,
      style: document.getElementById("style").value,
      length: document.getElementById("length").value,
    };

    try {
      const response = await fetch("/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      // Display Story
      storyTitleDisplay.textContent = data.title;
      storyContent.textContent = result.story;
      storySource.textContent = `Source: ${result.source}`;

      // Switch Views
      inputSection.style.display = "none";
      outputSection.style.display = "block";
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong! Please try again.");
    } finally {
      // Reset Button State
      generateBtn.disabled = false;
      btnText.textContent = "Generate Story";
      loader.style.display = "none";
    }
  });

  resetBtn.addEventListener("click", () => {
    outputSection.style.display = "none";
    inputSection.style.display = "block";
    form.reset();
  });
});
