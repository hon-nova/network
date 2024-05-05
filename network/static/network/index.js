document.addEventListener('DOMContendLoaded',()=>{
   //collect all heart-icon btns
   const likeBtns=document.querySelectorAll(".like-btn")

   likeBtns.forEach((btn)=>{
      btn.addEventListener('click',()=>{
         const postId=btn.dataset.postId

         fetch(`/likes/${postId}`,{
            method:"POST",
            headers:{
               "Content-Type":"application/json"
            },
         })
         .then(response=>response.json())
         .then(data=>{
            console.log('data::is it a dict? ',data)
            //update the likes_count
            const likesCountElement=document.querySelector(`#likes-count-${postId}`)
            likesCountElement.textContent=data.likes_count
         })
         .catch(err=>console.log('Tell me errors: ',err))
      })
   })
})