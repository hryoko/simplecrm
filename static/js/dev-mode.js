document.addEventListener("DOMContentLoaded", () => {
    // Devモードの状態を復元
  if (localStorage.getItem("dev-mode") === "true") {
    document.body.classList.add("dev-mode");
  }
  
  // Devモード切り替えボタン
  document.getElementById("toggle-dev-mode")?.addEventListener("click", () => {
    const isActive = document.body.classList.toggle("dev-mode");
    localStorage.setItem("dev-mode", isActive ? "true" : "false");
  });
});
