window.addEventListener('DOMContentLoaded', function(){
  timer = document.getElementsByClassName('timer')[0];
  timerHandle = setInterval(function(){
    timer.innerHTML = (parseInt(timer.innerHTML) - 1).toString();
    console.log(timer.innerHTML);
    if (timer.innerHTML <= 0) {
      clearInterval(timerHandle);
    }
  }, 1000, timer);
})
