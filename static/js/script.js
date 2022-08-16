document.addEventListener('DOMContentLoaded', () => {
    document.body.addEventListener('dragstart', drag);
    document.body.addEventListener('drop', drop);
    document.body.addEventListener('dragover', handleOver);
    document.getElementById("resetButton").addEventListener('click', handleClickReset);
});

function drag(ev){
    let obj = ev.target
    timestamp = Date.now();

    ev.dataTransfer.setData("time", timestamp);
    obj.setAttribute('data-ts', timestamp);
}

function drop(ev){
    let dropzone = ev.target;
    ev.preventDefault();
    let data = ev.dataTransfer.getData("time");
    let draggable = document.querySelector(`[data-ts="${data}"]`);

    if(!(dropzone.parentElement.classList.contains('dropzone') || dropzone.classList.contains('dropzone'))){
        if(draggable.getAttribute('clone') == "false") {
            draggable.remove();
            return;
        } else {
            return;
        }
    }
    
    if (draggable.getAttribute('clone') == "true") {
        let clone = draggable.cloneNode(true);
        clone.setAttribute('clone', "false");
        if (ev.target.classList.contains('dropzone')){
            dropzone.append(clone);
        } else {
            container = dropzone.parentElement;
            container.insertBefore(clone, dropzone);
        }
    } else if (draggable.getAttribute('clone') == "false") {
        if (ev.target.classList.contains('dropzone')){
            dropzone.append(draggable);
        } else {
            container = dropzone.parentElement;
            container.insertBefore(draggable, dropzone);
        }
    }
    dropzone.classList.remove('over');
    document.getElementById('algorithm_field').value = document.getElementById("algorithm").textContent;
    console.log(document.getElementById('algorithm_field').textContent)
}

function handleOver(ev){
    ev.preventDefault();
}

function handleClickReset(ev){
    ev.preventDefault();
    document.getElementById("algorithm").textContent = "OU_Prop_Stat";
}