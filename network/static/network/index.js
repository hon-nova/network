
document.addEventListener("DOMContentLoaded", () => {
  const likeBtns = document.querySelectorAll(".like-btn");

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

        let initialCountFromDb =document.querySelector(`#initial-count-${postId}`)
        // Update the likes count in the UI		 
        if (likesCountElement){
        
         likesCountElement.textContent = `${data.like_counts[postId]}`;
        }     
       
      } catch (error) {
        console.error("Error found::", error);
      }
    });
  });
});
