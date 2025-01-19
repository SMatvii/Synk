document.querySelectorAll('.delete-post-btn').forEach(btn => {
    btn.addEventListener('click', function (event) {
        event.preventDefault();
        const postId = this.dataset.postId;

        if (confirm('Are you sure you want to delete this post?')) {
            fetch(`/posts/delete/${postId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                },
            })
            .then(response => {
                if (response.ok) {
                    alert('Post deleted successfully!');
                    window.location.href = '/';
                } else {
                    alert('Failed to delete the post.');
                }
            });
        }
    });
});
