
    // Select all checkboxes in the left table
    document.getElementById('selectAllLeft').addEventListener('change', function() {
    document.querySelectorAll('.row-checkbox-left').forEach(checkbox => {
      checkbox.checked = this.checked;
    });
  });
