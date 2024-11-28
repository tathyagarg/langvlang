// fetch("http://0.0.0.0:8080/fetch?language=python", {
//   mode: 'no-cors'
// })
// .then(resp => resp.json())
// .then(data => console.log(data))
// .catch(err => console.error(err))

fetch("http://localhost:8080/fetch?language=python", {
  method: 'GET'
})
  .then(resp => resp.json())
  .then(data => {document.getElementById("py-vote").innerText = `Votes: ${data.votes}`})

console.log("hi!")
