document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.querySelector(".sidebar");
  const toggleButton = document.querySelector(".menu-button");

  if (!sidebar || !toggleButton) return;

  // 初期状態を復元
  if (localStorage.getItem("sidebar-collapsed") === "true") {
    sidebar.classList.add("collapsed");
  }

  // 開閉ボタンのイベント
  toggleButton.addEventListener("click", () => {
    sidebar.classList.toggle("collapsed");

    // 状態を保存
    const isCollapsed = sidebar.classList.contains("collapsed");
    localStorage.setItem("sidebar-collapsed", isCollapsed ? "true" : "false");
  });
});
