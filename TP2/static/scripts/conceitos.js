function delete_conceito(designation){ 
    $.ajax("/conceitos/"+ designation, {
        type:"DELETE",
        success: function(data) {
            console.log(data)
            if (data["success"]){
                alert("Conceito apagado com sucesso!");
                window.location.href = data["redirect_url"]
            }

        },
        error: function(error) {
            console.log(error)
            alert("Ocorreu um erro ao tentar apagar o conceito.");
        }
    })
}


function atualizar_conceito(formElement, designacao) {
    const formData = new FormData(formElement);

    $.ajax(`/conceitos/${designacao}/atualizar`, {
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            console.log(data);
            if (data["success"]) {
                alert("Conceito atualizado com sucesso!");
                window.location.href = data["redirect_url"];
            } else {
                alert(data["message"] || "Erro ao atualizar o conceito.");
            }
        },
        error: function (error) {
            console.error(error);
            alert("Ocorreu um erro ao atualizar o conceito.");
        }
    });
}


function adicionar_conceito(formElement) {
    const formData = new FormData(formElement);

    $.ajax("/conceitos", {
        method: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            if (data.success) {
                alert(data.message);
                window.location.href = data.redirect_url;
            } else {
                alert("Erro: " + data.message);
            }
        },
        error: function (err) {
            alert("Erro inesperado ao adicionar conceito.");
            console.log(err);
        }
    });
}



$(document).ready( function () {
    $('#conceitos').DataTable({
        search: {
            regex: true

        },

    });
});

$(document).ready( function () {
    $('#area_conceitos').DataTable({
        search: {
            regex: true

        },

    });
});
