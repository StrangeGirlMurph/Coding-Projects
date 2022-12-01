from qiskit import *
from qiskit import IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy


def random_qubit():
    IBMQ.load_account()
    provider = IBMQ.get_provider("ibm-q")

    small_devices = provider.backends(
        filters=lambda x: x.configuration().n_qubits == 5
        and not x.configuration().simulator
    )
    qcomp = least_busy(small_devices)

    qr = QuantumRegister(1)
    cr = ClassicalRegister(1)
    circuit = QuantumCircuit(qr, cr)

    circuit.h(0)
    circuit.measure(0, 0)

    job = execute(circuit, backend=qcomp, shots=1)
    job_monitor(job)

    return str(list(job.result().get_counts().keys())[0])


print(random_qubit())
