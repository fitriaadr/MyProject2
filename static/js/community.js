document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function () {
            const postId = this.getAttribute('data-post-id');
            const likeCountElement = document.getElementById(`like-count-${postId}`);
            const csrfToken = '{{ csrf_token }}';

            this.disabled = true;

            fetch(`/community/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if ('likes_count' in data) {
                    likeCountElement.textContent = data.likes_count; // Update jumlah like
                } else {
                    console.error('likes_count tidak ditemukan di respons JSON.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Terjadi kesalahan. Silakan coba lagi.');
            })
            .finally(() => {
                this.disabled = false;
            });
        });
    });
});
