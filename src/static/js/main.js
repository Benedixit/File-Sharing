function deleteProject(projectId) {
    if (confirm("Are you sure you want to delete this project?")) {
        var form = document.getElementById("deleteForm" + projectId);
        form.submit();
    }
}