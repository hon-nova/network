document.addEventListener('DOMContentLoaded',()=>{
   //collect all heart-icon btns
   const likeBtns=document.querySelectorAll(".like-btn")

   likeBtns.forEach((btn)=>{
      btn.addEventListener('click',()=>{
         const postId=btn.dataset.postId

         fetch(`/likes/${postId}`,{
            method:"POST",
            headers:{
               "Content-Type":"application/json",
               "X-CSRFToken":csrfToken
            },
            //include post.id in the headers
            body: JSON.stringify({postId:postId})
         })
         .then(response=>response.json())
         .then(data=>{
            alert('POST data sent from frontend::',data)
            console.log('data::is it a dict? ',data)
            //update the likes_count
            const likesCountElement=document.querySelector(`#likes-count-${postId}`)
            //from views.py
            likesCountElement.textContent=data.likes_count
            //change the color of the heart icon
            // if(data.is_liked){
            //    document.querySelector('.heart').style.color='red'
            // }
            //  else {
            //    document.querySelector('.heart').style.color='transparent'
            //  }
            const heartIcon = btn.querySelector('.heart');
                if (data.is_liked) {
                    heartIcon.style.color = 'red';
                } else {
                    heartIcon.style.color = 'black'; // Change to original color or transparent
                }
            console.log('likes_count::',likesCountElement.textContent)
         })
         .catch(err=>console.log('Tell me errors: ',err))
      })
   })
})