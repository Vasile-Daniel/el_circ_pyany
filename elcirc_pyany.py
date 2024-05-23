from django.shortcuts import render
###################################################################################3
import matplotlib
matplotlib.use('Agg')  # Setează backend-ul 'Agg' pentru Matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
from .forms import SimulationFormSimulationRLForm
import os
from django.conf import settings
import uuid
################### RC CIRCUIT #################################################
def run_simulation(voltage, resistance, capacitance, time_step, max_time):
    t = np.arange(0, max_time, time_step)
    Vc = voltage * (1 - np.exp(-t / (resistance * capacitance)))

    plt.figure()
    plt.plot(t, Vc, label=r'$ v_C (t) = E \cdot \left( 1 - e^{-\frac{t}{R \cdot C}}\right) $')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.title('Voltage across the Capacitor')
    plt.legend()
    plt.grid(True)

    # Salvarea figurii într-un director accesibil
    plot_file_name = f'rc_circuit_{uuid.uuid4().hex}.png'
    plot_file_path = os.path.join(settings.MEDIA_ROOT, plot_file_name)
    plt.savefig(plot_file_path)
    plt.close()

    # Returnarea căii relative a imaginii pentru a fi utilizată în template
    return os.path.join(settings.MEDIA_URL, plot_file_name)

################### RL CIRCUIT #################################################
def run_rl_simulation(voltage, resistance, inductance, time_step, max_time):
    t = np.arange(0, max_time, time_step)
    IL = (voltage / resistance) * (1 - np.exp(- (resistance * t) / inductance))

    plt.figure()
    plt.plot(t, IL, label=r'$ i_L (t) = \frac{E}{R} \cdot \left( 1 - e^{-\frac{R t}{L}}\right) $')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.title('Current through the Inductor')
    plt.legend()
    plt.grid(True)

    # Salvarea figurii într-un director accesibil
    plot_file_name = f'rl_circuit_{uuid.uuid4().hex}.png'
    plot_file_path = os.path.join(settings.MEDIA_ROOT, plot_file_name)
    plt.savefig(plot_file_path)
    plt.close()

    # Returnarea căii relative a imaginii pentru a fi utilizată în template
    return os.path.join(settings.MEDIA_URL, plot_file_name)

################### RC and RL CIRCUITS SIMULATIONS #################################################
def control(request):
    plot_file_url = None  # Inițializăm cu None pentru a gestiona cazul GET
    plot_file_url1 = None  # Inițializăm cu None pentru a gestiona cazul GET

    if request.method == 'POST':
        form = SimulationForm(request.POST)
        form1 = SimulationRLForm(request.POST)

        if form.is_valid():
            voltage = form.cleaned_data['voltage']
            resistance = form.cleaned_data['resistance']
            capacitance = form.cleaned_data['capacitance']
            time_step = form.cleaned_data['time_step']
            max_time = form.cleaned_data['max_time']
            plot_file_url = run_simulation(voltage, resistance, capacitance, time_step, max_time)

        if form1.is_valid():
            voltage = form1.cleaned_data['voltage']
            resistance = form1.cleaned_data['resistance']
            inductance = form1.cleaned_data['inductance']
            time_step = form1.cleaned_data['time_step']
            max_time = form1.cleaned_data['max_time']
            plot_file_url1 = run_rl_simulation(voltage, resistance, inductance, time_step, max_time)

    else:
        form = SimulationForm()
        form1 = SimulationRLForm()

    context = {'form': form, 'plot_file_url': plot_file_url, 'form1': form1, 'plot_file_url1': plot_file_url1}
    return render(request, 'control/rc_circuit_page.html', context)