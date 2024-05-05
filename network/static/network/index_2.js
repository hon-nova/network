

document.addEventListener('DOMContentLoaded',async (e)=>{
   //collect all heart-icon btns
   e.preventDefault()
   const likeBtns=document.querySelectorAll(".like-btn")
   
   likeBtns.forEach(function(btn){
     
      btn.addEventListener('click', async(e)=>{
         e.preventDefault()
         const postId=btn.dataset.postId
         console.log('postId::',postId)    
         
         // Retrieve stored like data from session
      console.log('{{ request.session.likes_data|escapejs }}');
      // const likeData = JSON.parse('{{ request.session.likes_data|escapejs }}');
      // document.querySelector(`#likes-count-${postId}`).innerHTML=`Number of likes: ${likeData.likes_count}`
      try {            
         await fetch(`/likes/${postId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ postId: postId })
            })
            .then(response=>response.json())
            .then(data=>{
                console.log('data::',data)

                console.log('JSON DATA::',data)
           
   
                const likesCountElement = document.querySelector(`#likes-count-${postId}`);
                likesCountElement.innerHTML = `Number of likes: ${data.likes_count}`;
   
                const heartIcon = btn.querySelector('.heart');
                heartIcon.style.color = data.is_liked ? 'red' : 'black';
   
                window.location.href = '/';
            })
        } catch (error) {
            console.error('Error found::', error);
        } 
      });     
    });
})
   //})
      //    fetch(`/likes/${postId}`,{
      //       method:"POST",
      //       headers:{
      //          "Content-Type":"application/json",
      //          "X-CSRFToken":csrfToken,
      //       },
      //       //include post.id in the headers
      //       body: JSON.stringify({postId:postId})
      //    })
      //    .then(response=>response.json())
      //    .then(data=>{
      //       // Alert after fetch
      //       alert('Data received from server: ' + JSON.stringify(data));
      //       alert('POST data sent from frontend::',data)
      //       console.log('data::is it a dict? ',data)
      //       //update the likes_count
      //       const likesCountElement=document.querySelector(`#likes-count-${postId}`)
      //       //from views.py
      //       likesCountElement.textContent= `Number of likes: ${data.likes_count}`;
           
      //       const heartIcon = btn.querySelector('.heart');
      //           if (data.is_liked) {
      //               heartIcon.style.color = 'red';
      //           } else {
      //               heartIcon.style.color = 'black'; 
      //           }
      //       console.log('likes_count::',likesCountElement.textContent)
      //    })
      //    .catch(err=>console.log('Tell me errors: ',err))
      // })
  // })
//})