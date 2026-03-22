const PAGE_2 = "/page2";

function checkWebsite() {
  const input = document.getElementById("urlInput");
  const result = document.getElementById("result");
  const url = input.value.trim();

  result.className = "result";
  result.classList.remove("hidden");

  if (!isValidURL(url)) {
    result.textContent = "Invalid URL format";
    result.classList.add("error");
    return;
  }

  result.textContent = "Analyzing URL...";
  result.classList.add("safe");

  setTimeout(() => {
    window.location.href = `${PAGE_2}?url=${encodeURIComponent(url)}`;
  }, 1200);
}

function isValidURL(url) {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}
