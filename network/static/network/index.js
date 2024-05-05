// document.addEventListener("DOMContentLoaded", async (e) => {
//   //collect all heart-icon btns
//   e.preventDefault();
//   const likeBtns = document.querySelectorAll(".like-btn");
//   likeBtns.forEach(function (btn) {
//     btn.addEventListener("click", async (e) => {
//       e.preventDefault();
//       const postId = btn.dataset.postId;

//       try {
//         let response = await fetch(`/likes/${postId}`, {
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json",
//             "X-CSRFToken": csrfToken,
//           },
//           body: JSON.stringify({ postId: postId }),
//         });
//         console.log("response::", response);
//         console.log("response.status::", response.status);
       
//         if (response.status !== 200) {
//           throw new Error("Network response was not ok");
//         }
//         data = await response.json();

//         console.log("JSON DATA::", data);

//         const likesCountElement = document.querySelector(
//           `#likes-count-${postId}`
//         );
//         likesCountElement.innerHTML = `Number of likes: ${data.likes_count}`;

//         const heartIcon = btn.querySelector(".heart");
//         heartIcon.style.color = data.is_liked ? "red" : "black";
        
//       } catch (error) {
//         console.error("Error found::", error);
//       }
//     });
//   });
// });


// document.addEventListener("DOMContentLoaded", async () => {
//     const likeBtns = document.querySelectorAll(".like-btn");
    
//     // Function to update like count and heart icon color
//     const updateLikeInfo = async (postId, isLiked) => {
//         try {
//             const response = await fetch(`/likes/${postId}`, {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                     "X-CSRFToken": csrfToken
//                 },
//                 body: JSON.stringify({ postId: postId })
//             });

//             if (!response.ok) {
//                 throw new Error("Network response was not ok");
//             }

//             const data = await response.json();

//             console.log(`DATA::${data}`)

//             const likesCountElement = document.querySelector(`#likes-count-${postId}`);
//             likesCountElement.textContent = `Number of likes: ${data.likes_count}`;

//             let heartIcon = document.querySelector(`#heart-icon-${postId}`);
//             heartIcon.style.color = data.is_liked ? "red" : "black";
//         } catch (error) {
//             console.error("Error updating like info:", error);
//         }
//     };

//     // Event listener for like button clicks
//     likeBtns.forEach(btn => {
//         btn.addEventListener("click", async () => {
//             const postId = btn.dataset.postId;
//             const isLiked = btn.classList.contains("liked");

//             // Update like info based on current like status
//             await updateLikeInfo(postId, isLiked);

//             // Toggle liked class on button
//             btn.classList.toggle("liked");
//         });
//     });

//     // Fetch and display like count for each post on page load
//     const postIds = Array.from(likeBtns).map(btn => btn.dataset.postId);
//     postIds.forEach(postId => {
//         updateLikeInfo(postId);
//     });
// });

document.addEventListener("DOMContentLoaded", () => {

    const likeBtns = document.querySelectorAll(".like-btn");
  
    likeBtns.forEach((btn) => {
        const postId = btn.dataset.postId;
         //retrieve localStorage
         document.querySelector(`#likes-count-${postId}`).innerHTML=localStorage.getItem('likes_count')
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
          //step 1:  
        if (!localStorage.getItem('likes_count')){
            localStorage.setItem('likes_count','')
        }
        const data = await response.json();

        console.log('DATA::',data)
        const likesCountElement = document.querySelector(`#likes-count-${postId}`);
        const heartIcon = btn.querySelector(".heart");
  
          // Toggle the liked class on the button
        btn.classList.toggle("liked");
  
          // Update the heart icon color based on like status
        heartIcon.style.color = data.is_liked ? "red" : "black";
  
        // Update the likes count in the UI
        likesCountElement.textContent = `${data.likes_count}`;
        //save to localStorage         
        //step 2:
        let count=0

        if(localStorage.getItem('likes_count')){
            count=parseInt(JSON.parse(localStorage.getItem('likes_count')))
        }
        count=data.likes_count
        localStorage.setItem('likes_count',JSON.stringify(count))

        } catch (error) {
          console.error("Error found:", error);
        }
      });
    });
  });
  

