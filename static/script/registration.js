$(document).ready(function () {
  // Handle error message removal
  $(document).on(
    "input",
    "form input, form select, form textarea",
    function () {
      var field = $(this);
      var errorElement = $("#error-" + field.attr("name"));
      if (errorElement.length > 0) {
        errorElement.fadeOut(2000, function () {
          $(this).remove();
        });
      }
    }
  );
});
