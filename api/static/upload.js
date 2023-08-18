const browsefile = document.querySelector(".browsefile");

browsefile.addEventListener("dragover", (e) => {
  e.preventDefault()
  browsefile.classList.add("hover");
 
});

browsefile.addEventListener("dragleave", () => {
  browsefile.classList.remove("hover");
});

browsefile.addEventListener("drop", (e) => {
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
    browsefile.setAttribute("class", "browsefile invalid");
    browsefile.innerText = "Invalid File Format!";
    return false;
  }
});

const upload = (file) => {
  browsefile.setAttribute("class", "browsefile valid");
  browsefile.innerText = "Added " + file.name;
};