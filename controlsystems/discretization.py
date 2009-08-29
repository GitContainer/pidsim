"""Discretization module

This module implements some numerical methods to discretize Transfer
Functions.

"""

__all__ = ['Euler', 'RungeKutta2', 'RungeKutta3', 'RungeKutta4']

#TODO: discretize State-Space models too.
#TODO: implement more numerical methods

from types import Matrix, ZerosMatrix, IdentityMatrix, \
                  TransferFunction, StateSpace
from error import ControlSystemsError

def Euler(g, sample_time, total_time):
    """Euler Method
    
    Returns points of step response of the transfer function 'g',
    discretized with Euler method, using sample time 'sample_time'
    on 'total_time' seconds. For example:
    
        >>> g = TransferFunction([1], [1, 2, 3])
        >>> t, y = Euler(g, 0.01, 10)
        >>> print t
        (prints an vector of times 0-10s, with sample time 0.01s)
        >>> print y
        (prints an vector of points, with same size of 't')
    
    """
    
    if not isinstance(g, TransferFunction):
        raise ControlSystemsError('Parameter must be a Transfer Fcn.')

    ss = StateSpace(g)
    
    samples = int(total_time/sample_time) + 1
    
    t = [sample_time * a for a in range(samples)]
    
    x = ZerosMatrix(ss.a.rows, 1)
    y = []
    
    eye = IdentityMatrix(ss.a.rows)
    
    a1 = eye + ss.a.mult(sample_time)
    a2 = ss.b.mult(sample_time)
    
    for i in range(samples):
        x = a1*x + a2
        y.append((ss.c*x)[0][0] + ss.d[0][0])

    return t, y


def RungeKutta2(g, sample_time, total_time):
    """RungeKutta2 Method
    
    Returns points of step response to the transfer function 'g',
    discretized with Runge Kutta (order 2) method, using sample time
    'sample_time' on 'total_time' seconds, like:
    
        >>> g = TransferFunction([1], [1, 2, 3])
        >>> t, y = RungeKutta2(g, 0.01, 10)
        >>> print t
        (prints an vector of times 0-10s, with sample time 0.01s)
        >>> print y
        (prints an vector of points, with same size of 't')
    
    """
    
    if not isinstance(g, TransferFunction):
        raise ControlSystemsError('Parameter must be a Transfer Fcn.')

    ss = StateSpace(g)
    
    samples = int(total_time/sample_time) + 1
    
    t = [sample_time * a for a in range(samples)]
    
    x = ZerosMatrix(ss.a.rows, 1)
    y = []
    
    eye = IdentityMatrix(ss.a.rows)
    
    a1 = ss.a * ss.a
    a2 = ss.a.mult(2) + a1.mult(sample_time)
    a3 = a2.mult(0.5)
    a4 = ss.a.mult(sample_time)
    a5 = a4*ss.b + ss.b.mult(2)
    a6 = eye + a3.mult(sample_time)
    a7 = a5.mult(sample_time/2)
    
    for i in range(samples):
        x = a6*x + a7
        y.append((ss.c*x)[0][0] + ss.d[0][0])

    return t, y


def RungeKutta3(g, sample_time, total_time):
    """RungeKutta3 Method
    
    Returns points of step response to the transfer function 'g',
    discretized with Runge Kutta (order 3) method, using sample time
    'sample_time' on 'total_time' seconds, like:
    
        >>> g = TransferFunction([1], [1, 2, 3])
        >> t, y = RungeKutta3(g, 0.01, 10)
        >>> print t
        (prints an vector of times 0-10s, with sample time 0.01s)
        >>> print y
        (prints an vector of points, with same size of 't')
    
    """
    
    if not isinstance(g, TransferFunction):
        raise ControlSystemsError('Parameter must be a Transfer Fcn.')

    ss = StateSpace(g)
    
    samples = int(total_time/sample_time) + 1
    
    t = [sample_time * a for a in range(samples)]
    
    x = ZerosMatrix(ss.a.rows, 1)
    y = []
    
    eye = IdentityMatrix(ss.a.rows)
    
    a1 = ss.a.mult(sample_time) # A*T
    a2 = ss.b.mult(sample_time) # B*T
    a3 = (ss.a * ss.a).mult(sample_time * sample_time) # A^2*T^2
    a4 = a3.mult(0.5) # (A^2*T^2)/2
    a5 = (ss.a * ss.b).mult(sample_time * sample_time) # A*B*T^2
    a6 = a5.mult(0.5) # (A*B*T^2)/2
    a7 = a3.mult(3.0/4.0) # (A^2*T^2)*(3/4)
    a8 = (ss.a*ss.a*ss.a).mult(sample_time * sample_time * sample_time)
    a9 = a8.mult(3.0/8.0)
    a10 = (ss.a*ss.a*ss.b).mult(sample_time * sample_time * sample_time)
    a11 = a10.mult(3.0/8.0)
    a12 = a5.mult(3.0/4.0) + a2
    
    for i in range(samples):
        k1 = a1*x + a2
        k2 = (a1 + a4)*x + a6 + a2
        k3 = (a1 + a7 + a9)*x + a11 + a12
        
        x = x + (k1.mult(2.0/9.0) + k2.mult(1.0/3.0) + k3.mult(4.0/9.0))
        
        y.append((ss.c*x)[0][0] + ss.d[0][0])

    return t, y


def RungeKutta4(g, sample_time, total_time):
    """RungeKutta4 Method
    
    Returns points of step response to the transfer function 'g',
    discretized with Runge Kutta (order 4) method, using sample time
    'sample_time' on 'total_time' seconds, like:
    
        >>> g = TransferFunction([1], [1, 2, 3])
        >>> t, y = RungeKutta4(g, 0.01, 10)
        >>> print t
        (prints an vector of times 0-10s, with sample time 0.01s)
        >>> print y
        (prints an vector of points, with same size of 't')
    
    """
    
    if not isinstance(g, TransferFunction):
        raise ControlSystemsError('Parameter must be a Transfer Fcn.')

    ss = StateSpace(g)
    
    samples = int(total_time/sample_time) + 1
    
    t = [sample_time * a for a in range(samples)]
    
    x = ZerosMatrix(ss.a.rows, 1)
    y = []
    
    eye = IdentityMatrix(ss.a.rows)
    
    a1 = ss.a.mult(sample_time) # A*T
    a2 = ss.b.mult(sample_time) # B*T
    a3 = (ss.a * ss.a).mult(sample_time * sample_time) # A^2*T^2
    a4 = a3.mult(0.5) # (A^2*T^2)/2
    a5 = (ss.a * ss.b).mult(sample_time * sample_time) # A*B*T^2
    a6 = a5.mult(0.5) # (A*B*T^2)/2
    a7 = (ss.a*ss.a*ss.a).mult(sample_time * sample_time * sample_time)
    a8 = a7.mult(0.25)
    a9 = (ss.a*ss.a*ss.b).mult(sample_time * sample_time * sample_time)
    a10 = a9.mult(0.25)
    a11 = a7.mult(0.5)
    a12 = (ss.a*ss.a*ss.a*ss.a).mult(sample_time * sample_time * \
           sample_time * sample_time)
    a13 = a12.mult(0.25)
    a14 = ss.a.mult(sample_time * sample_time)
    a15 = a14*ss.b
    a16 = a9.mult(0.5)
    a17 = (ss.a*ss.a*ss.a*ss.b).mult(sample_time * sample_time * \
           sample_time * sample_time)
    a18 = a17.mult(0.25)
    
    for i in range(samples):
        k1 = a1*x + a2
        k2 = (a1 + a4)*x + a6 + a2
        k3 = (a1 + a4 + a8)*x + a2 + a6 + a10;
        k4 = (a1 + a3 + a11 + a13)*x + a15 +a16 + a18 + a2
        
        x = x + k1.mult(1.0/6.0) + k2.mult(1.0/3.0) + k3.mult(1.0/3.0) \
              + k4.mult(1.0/6.0)
        
        y.append((ss.c*x)[0][0] + ss.d[0][0])

    return t, y