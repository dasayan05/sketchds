import matplotlib.pyplot as plt
import numpy as np
from scipy.special import comb as choose

def bezier_matrix(degree):
    m = degree
    Q = np.zeros((degree + 1, degree + 1))
    for i in range(degree + 1):
        for j in range(degree + 1):
            if (0 <= (i+j)) and ((i+j) <= degree):
                Q[i,j] = choose(m, j) * choose(m-j, m-i-j) * ((-1)**(m-i-j))
    return Q

def bij(t, i, n):
    # binomial coefficients
    return choose(n, i) * (t ** i) * ((1-t) ** (n-i))


def draw_bezier(ctrlPoints, nPointsCurve=100, curvePlotKwagrs=dict(color='g'), draw_axis=plt):
    '''
    Draws a Bezier curve with given control points

    ctrlPoints: shape (n+1, 2) matrix containing all control points
    nPointsCurve: granularity of the Bezier curve

    ctrlPointPlotKwargs: The **kwargs for control point's plot() function
    curvePlotKwagrs: The **kwargs for curve's plot() function
    '''

    nCtrlPoints = ctrlPoints.shape[0]

    def T(ts: 'time points', d: 'degree'):
        # 'ts' is a vector (np.array) of time points
        ts = ts[..., np.newaxis]
        Q = tuple(ts**n for n in range(d, -1, -1))
        return np.concatenate(Q, 1)

    ts = np.linspace(0., 1., num=nPointsCurve)

    curve = np.matmul(
        T(ts, nCtrlPoints - 1),
        np.matmul(
            bezier_matrix(nCtrlPoints-1),
            ctrlPoints
        )
    )

    draw_axis.plot(curve[:, 0], curve[:, 1], **curvePlotKwagrs)
