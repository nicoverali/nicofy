window.addEventListener('DOMContentLoaded', function(){
  //Add copy to clipboard feature
  copyButtonObject = new Clipboard('.copy'); //This uses clipboard.js from Zeno Rocha
  copyButton = document.getElementsByClassName('copy')[0];
  copyButtonObject.on('success',function(){
    copyButton.classList.remove('finish-copy')
    copyButton.classList.add('copied');
    setTimeout(function(){
      copyButton.classList.remove('copied')
      copyButton.classList.add('finish-copy')
    }, 2000)
  })
})
