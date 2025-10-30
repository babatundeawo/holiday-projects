function goTo(page) {
  if (!page || typeof page !== 'string') {
    console.error('Invalid page parameter');
    return;
  }
  if (window.location.assign) {
    window.location.assign(page);
  } else {
    window.location.href = page;
  }
}

// Optional: smooth scroll for anchor links or back-to-top button in future
document.addEventListener("DOMContentLoaded", () => {
  console.log("Holiday Projects site ready.");
});
