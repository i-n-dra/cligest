async function run_validacion() {
  const run_input = document.getElementById("id_run_rep_legal");
  const run_help_text = document.getElementById("id_run_rep_legal_helptext");
  const run = run_input.value.trim();
  if (!run) return;

  const response = await fetch(`run-validacion/?run=${encodeURIComponent(run)}`);
  const data = await response.json();

  if (data.exists) {
    run_help_text.textContent = "El RUN ya está registrado";
    run_help_text.style.color = "red";
  } else {
    regex = /^\d{7,8}-[\dkK]$/;
    match = run.match(regex);
    if (!match) {
      run_help_text.textContent = "El formato del RUN es incorrecto";
      run_help_text.style.color = "red";
    } else {
      run_help_text.textContent = "RUN disponible";
      run_help_text.style.color = "green";
    }
  }
}

async function rut_validacion() {
  const rut_input = document.getElementById("id_run_empresa");
  const rut_help_text = document.getElementById("id_run_empresa_helptext");
  const rut = rut_input.value.trim();
  if (!rut) return;

  const response = await fetch(`rut-validacion/?rut=${encodeURIComponent(rut)}`);
  const data = await response.json();

  if (data.exists) {
    rut_help_text.textContent = "El RUN/RUT ya está registrado";
    rut_help_text.style.color = "red";
  } else {
    regex = /^\d{7,8}-[\dkK]$/;
    match = rut.match(regex);
    if (!match) {
      rut_help_text.textContent = "El formato del RUN/RUT es incorrecto";
      rut_help_text.style.color = "red";
    } else {
      rut_help_text.textContent = "RUN/RUT disponible";
      rut_help_text.style.color = "green";
    }
  }
}

async function suma_pagos() {
  let input_iva1 = document.getElementById("id_iva_a_pagar");
  let input_iva2 = document.getElementById("id_iva_anticipado");
  let input_ppm_vehiculo = document.getElementById("id_ppm_vehiculo");
  let input_ppm_ventas = document.getElementById("id_ppm_ventas");
  let input_honorarios = document.getElementById("id_honorarios");
  let input_f301 = document.getElementById("id_f301");
  let input_imposiciones = document.getElementById("id_imposiciones");
  let input_otros = document.getElementById("id_otros");
  let input_a_pagar = document.getElementById("id_a_pagar");
  let input_total = document.getElementById("id_total");

  const inputs = [
    input_iva1, input_iva2, input_ppm_vehiculo, input_ppm_ventas,
    input_honorarios, input_f301, input_imposiciones, input_otros, input_total
  ];

  inputs.forEach(input => {
    if (isNaN(parseInt(input.value))) {
      input.value = 0;
    }
  });
  
  let total = 0;
  total +=
    parseInt(input_iva1.value) +
    parseInt(input_ppm_vehiculo.value) +
    parseInt(input_ppm_ventas.value) +
    parseInt(input_honorarios.value) +
    parseInt(input_f301.value) + 
    parseInt(input_imposiciones.value) +
    parseInt(input_otros.value) +
    parseInt(input_iva2.value);

  input_total.value = total;

  total -= parseInt(input_iva2.value);

  input_a_pagar.value = total;
}