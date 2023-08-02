const courseClick = document.querySelector('.courseclick')
const right_coloumn = document.querySelector('.right_coloumn')
const addCourse_wrapper = document.querySelector('.addcourse_form_wrapper')
const addCourse_wrapper_id = document.getElementById('addcourse_form_wrapper')
const submit = document.querySelector('.submit')
const allCourses = document.getElementById('courses')
const course_name_input = document.querySelector('.course_name_input')
const course_name_output = document.querySelector('.course_name_output')
const left_coloumn = document.querySelector('.left_coloumn')
const dots = document.querySelectorAll('.dots')
const year_input =document.querySelector('.year_input')
const year_output = document.querySelector('.year_output')
const perCourse = document.getElementById('course1')
const one_course = document.querySelectorAll('.course1')
const everyCourse = document.querySelectorAll('.courses')
let count = 0
const trash = document.querySelectorAll('.trash')
Number(count)



function addingcourses(){
    courseClick.addEventListener("click", ()=>{
        addCourse_wrapper.classList.add("show")
        
        right_coloumn.classList.add("blur")
        left_coloumn.classList.add("blur")


    })
    
    
}



addingcourses()

function submitFields(){
    submit.addEventListener("click",()=>{
        addCourse_wrapper.classList.remove("show")
        removeText()
        
        
        
        console.log(count)
    })

}
submitFields()



function removeText(){
    const text = document.querySelector('.middle')
    console.log(course_name_input.value)
    console.log(year_input.value)
    if(course_name_input.value!="" && year_input.value!=""){
        console.log("done")
        text.classList.add("hidden")
        takeCourseInput()
        takeYearInput()
        count++
        createNewCourse()
        blur()
    }else{
        alert("PLEASE ENTER COURSE NAME OR CLASS!!")
        
        blur()
    }
    

}

function takeCourseInput(){
 
    course_name_output.innerText = course_name_input.value.toUpperCase()
    console.log(course_name_input.value)
    course_name_input.value=""
}

function takeYearInput(){
   
    year_output.innerText = year_input.value.toUpperCase()
    console.log(year_input.value)
    year_input.value=""
}







function createNewCourse(){
   
   
    const deepCopy = perCourse.cloneNode(true);
    deepCopy.classList.remove("sample_course")
    deepCopy.classList.add("course1")


    trash.forEach(button =>{
        button.addEventListener("click", (e)=>{
            const buttonPiece = e.target
            console.log(buttonPiece.innerText)
        })
    })


    deepCopy.classList.add("newclass")
    
    
   
    takeCourseInput()
    takeYearInput()
    allCourses.appendChild(deepCopy);
    console.log("working")
    allCourses.classList.remove("hidden")
    



    
   
}

function blur(){
    right_coloumn.classList.remove("blur")
    left_coloumn.classList.remove("blur")
}

const newclass = document.querySelector('.newclass')



document.onclick=function(event){
    var container = addCourse_wrapper_id;
    console.log(event)
    console.log(event.target.matches('.addcourse_form_wrapper'));
    console.log(event.target.classList.contains("addcourse_form_wrapper"))
    console.log(container.style.flex);
    if(addCourse_wrapper_id.classList.contains('show'))
    {
        if(event.target.matches('.addcourse_form_wrapper') && !event.target.classList.contains("addcourse_form_wrapper") && event.target.classList.contains("courseclick") && event.target.matches('courseclick')){
            container.classList.remove("show");
            blur()
        }
        
    }   
}
