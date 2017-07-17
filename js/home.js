window.addEventListener('DOMContentLoaded', function(){
  //Assign variables to elements in DOM
  pageURL = document.getElementsByClassName('page-url-input')[0];
  pageURLAlert = document.getElementsByClassName('alert-message')[0];
  userContainer = document.getElementsByClassName('user')[0];
  user = document.getElementsByClassName('username-input')[0];
  userAlert = document.getElementsByClassName('alert-message')[1];
  submit = document.getElementsByClassName('submit-input')[0];

  //Check for input and out-of-focus for PAGE URL
  didWriteOnPage = false;
  pageURL.addEventListener('input', function(){
    didWriteOnPage = true;
    userInput = pageURL.value;
    if (checkForUrl(userInput)){
      user.disabled = false;
      userContainer.classList.add('show');
      alertMessage('pageURL', false)
    }
    checkForSubmit(userInput, user.value);
  })
  pageURL.addEventListener('focusout', function(){
     if (didWriteOnPage){
       userInput = (pageURL.value)
       if (!checkForUrl(userInput)) {
         alertMessage('pageURL', true)
       }
     }
  })

  //Check for input and out-of-focus for USERNAME
  didWriteOnUser = false;
  user.addEventListener('input', function(){
    didWriteOnUser = true;
    userInput = user.value;
    if (checkForName(userInput)){
      submit.classList.add('show')
      alertMessage('user', false)
    }
    checkForSubmit(pageURL.value, userInput);
  })
  user.addEventListener('focusout', function(){
     if (didWriteOnUser){
       userInput = (user.value)
       if (!checkForName(userInput)) {
         alertMessage('user', true)
       }
     }
  })

})

function checkForUrl(url){
  regex = /^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$/gm;
  match = regex.exec(url);
  if ((match != null) && (match[0] == url)){
    return true;
  }
  return false;
}

function checkForName(name){
  if ((name.length >= 6) && (name.length <= 20)){
    return true;
  }
  return false;
}

function checkForSubmit(urlInput, usernameInput){
  if (!checkForUrl(urlInput) || !checkForName(usernameInput)){
    submit.disabled = true;
    return;
  }
  submit.disabled = false;
}

function alertMessage(inputType, action){
  switch (inputType) {
    case 'pageURL':
      pageURLAlert.classList.toggle('show', action);
      pageURLAlert.classList.toggle('non-selectable', action);
      break;
    case 'user':
      userAlert.classList.toggle('show', action);
      userAlert.classList.toggle('non-selectable', action);
      break;
  }
}
