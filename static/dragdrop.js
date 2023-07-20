const droparea = document.querySelector(".droparea");

droparea.addEventListener("dragover", (e) => {
  e.preventDefault()
  droparea.classList.add("hover");
 
});

droparea.addEventListener("dragleave", () => {
  droparea.classList.remove("hover");
});

droparea.addEventListener("drop", (e) => {
  e.preventDefault();

  const file = e.dataTransfer.files[0];
  const type = file.type;

  if (
    type != "image/png" ||
    type != "image/jpg" ||
    type != "image/jpeg"
  ) {
    return upload(file);
  } else {
    droparea.setAttribute("class", "droparea invalid");
    droparea.innerText = "Invalid File Format!";
    return false;
  }
});

const upload = (file) => {
  droparea.setAttribute("class", "droparea valid");
  droparea.innerText = "Added " + file.name;
};