
document.addEventListener("DOMContentLoaded", () => {
  const likeBtns = document.querySelectorAll(".like-btn");
  //step 1: get localStorage
  let likeCounts = JSON.parse(localStorage.getItem('like_counts')) || {}; 

  for (const postId in likeCounts) {
    const likesCountElement = document.querySelector(`#likes-count-${postId}`);
    if (likesCountElement) {
      likesCountElement.textContent = likeCounts[postId];
    }
  }

  likeBtns.forEach((btn) => {
    const postId = btn.dataset.postId;
    
    btn.addEventListener("click", async () => {
      try {
        const response = await fetch(`/likes/${postId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ postId: postId }),
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }    
        const data = await response.json();
        console.log("DATA::", data); 
        const likesCountElement = document.querySelector(
          `#likes-count-${postId}`
        )        
        // Update the likes count in the UI		 
        if (likesCountElement){        
         likesCountElement.textContent = `${data.like_counts[postId]}`;
         
        }    
      //   console.log('data.like-counts::',data.like_counts) 

      likeCounts[postId] = data.like_counts[postId];
       
      localStorage.setItem('like_counts', JSON.stringify(likeCounts));
       
      } catch (error) {
        console.error("Error found::", error);
      }
    });
  });
});
