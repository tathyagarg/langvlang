fetch("http://0.0.0.0:8000/fetch?language=python")
  .then(resp => {
    if (!resp.ok) {
      throw new Error(`Response not ok.`)
    }

    return resp.json()
  }).then(data => {
    console.log(data);
  })
