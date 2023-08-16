const ise = document.querySelector(".ise")
const ese = document.querySelector(".ese")
const total = document.querySelector(".tot")


ise.addEventListener("click",()=>{
    ise.classList.add("show")
    ese.classList.add("hidden")
    total.classList.add("hidden")
})
ese.addEventListener("click",()=>{
    ese.classList.add("show")
    ise.classList.add("hidden")
    total.classList.add("hidden")
})
tot.addEventListener("click",()=>{
    tot.classList.add("show")
    ese.classList.add("hidden")
    ise.classList.add("hidden")
})


