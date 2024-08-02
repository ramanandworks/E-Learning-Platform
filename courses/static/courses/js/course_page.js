var player
var video_list

// window.onload=()=>{
//     player=document.getElementById('player')
//     maintainratio()
// }

document.onreadystatechange=function(){
    if(document.readyState=='interactive') {
        player=document.getElementById('player')
        video_list=document.getElementById('video_list')
        // video_list.style.maxHeight
        maintainratio()
    }
}

function maintainratio()
{
    var w=player.clientWidth
    var h=(w*9)/16
    player.height=h
    video_list.style.maxHeight=h + "px"
}

window.onresize=maintainratio
