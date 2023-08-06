from aerosandbox.common import *
from aerosandbox import Opti
import aerosandbox.numpy as np
from aerosandbox.dynamics.equations_of_motion import equations_of_motion
from aerosandbox import OperatingPoint, Atmosphere
from typing import Union


class FreeBodyDynamics(AeroSandboxObject):
    def __init__(self,
                 xe: Union[np.ndarray, float] = None,
                 ye: Union[np.ndarray, float] = None,
                 ze: Union[np.ndarray, float] = None,
                 u: Union[np.ndarray, float] = None,
                 v: Union[np.ndarray, float] = None,
                 w: Union[np.ndarray, float] = None,
                 phi: Union[np.ndarray, float] = None,
                 theta: Union[np.ndarray, float] = None,
                 psi: Union[np.ndarray, float] = None,
                 p: Union[np.ndarray, float] = None,
                 q: Union[np.ndarray, float] = None,
                 r: Union[np.ndarray, float] = None,
                 X=0,
                 Y=0,
                 Z=0,
                 L=0,
                 M=0,
                 N=0,
                 mass=1,
                 Ixx=1,
                 Iyy=1,
                 Izz=1,
                 Ixy=0,
                 Iyz=0,
                 Ixz=0,
                 g=0,
                 hx=0,
                 hy=0,
                 hz=0,
                 opti_to_add_constraints_to: Opti = None,
                 time: np.ndarray = None,
                 ):

        self.xe = 0 if xe is None else xe
        self.ye = 0 if ye is None else ye
        self.ze = 0 if ze is None else ze
        self.u = 0 if u is None else u
        self.v = 0 if v is None else v
        self.w = 0 if w is None else w
        self.phi = 0 if phi is None else phi
        self.theta = 0 if theta is None else theta
        self.psi = 0 if psi is None else psi
        self.p = 0 if p is None else p
        self.q = 0 if q is None else q
        self.r = 0 if r is None else r
        self.X = X
        self.Y = Y
        self.Z = Z
        self.L = L
        self.M = M
        self.N = N
        self.mass = mass
        self.Ixx = Ixx
        self.Iyy = Iyy
        self.Izz = Izz
        self.Ixy = Ixy
        self.Iyz = Iyz
        self.Ixz = Ixz
        self.g = g
        self.hx = hx
        self.hy = hy
        self.hz = hz
        self.time = time

        if opti_to_add_constraints_to is not None:
            if time is None:
                raise ValueError("`time` parameter must be an array-like if `opti_to_add_constraints_to` is given!")

            state = self.state
            state_derivatives = self.state_derivatives()
            for k in state.keys():  # TODO default to second-order integration for position, angles
                if locals()[k] is None:  # Don't constrain states that haven't been defined by the user.
                    continue
                try:
                    opti_to_add_constraints_to.constrain_derivative(
                        derivative=state_derivatives[k],
                        variable=state[k],
                        with_respect_to=self.time,
                    )
                except Exception as e:
                    raise ValueError(f"Error while constraining state variable `{k}`: \n{e}")

    def __repr__(self):
        repr = []
        repr.append("Dynamics instance:")

        def trim(string, width=40):
            string = string.strip()
            if len(string) > width:
                return string[:width - 3] + "..."
            else:
                return string

        def makeline(k, v):
            name = trim(str(k), width=8).rjust(8)
            item = trim(str(v), width=40).ljust(40)

            try:
                value = str(self.opti.value(v))
            except:
                value = None

            if str(value).strip() == str(item).strip():
                value = None

            if isinstance(v, float) or isinstance(v, int) or isinstance(v, np.ndarray):
                value = None

            if value is not None:
                value = trim(value, width=40).ljust(40)
                return f"\t\t{name}: {item} ({value})"
            else:
                return f"\t\t{name}: {item}"

        repr.append("\tState variables:")
        for k, v in self.state.items():
            repr.append(makeline(k, v))

        repr.append("\tControl/other variables:")
        for k, v in self.control_variables.items():
            repr.append(makeline(k, v))

        return "\n".join(repr)

    # TODO add __getitem__ for dynamic state at instant in time

    @property
    def state(self):
        return {
            "xe"   : self.xe,
            "ye"   : self.ye,
            "ze"   : self.ze,
            "u"    : self.u,
            "v"    : self.v,
            "w"    : self.w,
            "phi"  : self.phi,
            "theta": self.theta,
            "psi"  : self.psi,
            "p"    : self.p,
            "q"    : self.q,
            "r"    : self.r,
        }

    def state_derivatives(self):
        return equations_of_motion(
            xe=self.xe,
            ye=self.ye,
            ze=self.ze,
            u=self.u,
            v=self.v,
            w=self.w,
            phi=self.phi,
            theta=self.theta,
            psi=self.psi,
            p=self.p,
            q=self.q,
            r=self.r,
            X=self.X,
            Y=self.Y,
            Z=self.Z,
            L=self.L,
            M=self.M,
            N=self.N,
            mass=self.mass,
            Ixx=self.Ixx,
            Iyy=self.Iyy,
            Izz=self.Izz,
            Ixy=self.Ixy,
            Iyz=self.Iyz,
            Ixz=self.Ixz,
            g=self.g,
            hx=self.hx,
            hy=self.hy,
            hz=self.hz,
        )

    @property
    def control_variables(self):
        return {
            "X"       : self.X,
            "Y"       : self.Y,
            "Z"       : self.Z,
            "L"       : self.L,
            "M"       : self.M,
            "N"       : self.N,
            "mass"    : self.mass,
            "Ixx"     : self.Ixx,
            "Iyy"     : self.Iyy,
            "Izz"     : self.Izz,
            "Ixy"     : self.Ixy,
            "Iyz"     : self.Iyz,
            "Ixz"     : self.Ixz,
            "g"       : self.g,
            "hx"      : self.hx,
            "hy"      : self.hy,
            "hz"      : self.hz,
            "alpha"   : self.alpha,
            "beta"    : self.beta,
            "speed"   : self.speed,
            "altitude": self.altitude
        }

    @property
    def alpha(self):
        """The angle of attack, in degrees."""
        return np.arctan2d(
            self.w,
            self.u
        )

    @property
    def beta(self):
        """The sideslip angle, in degrees."""
        return np.arctan2d(
            self.v,
            (self.u ** 2 + self.w ** 2) ** 0.5
        )

    @property
    def speed(self):
        """The speed of the object, expressed as a scalar."""
        return (
                       self.u ** 2 +
                       self.v ** 2 +
                       self.w ** 2
               ) ** 0.5

    @property
    def translational_kinetic_energy(self):
        speed_squared = (
                self.u ** 2 +
                self.v ** 2 +
                self.w ** 2
        )
        return 0.5 * self.mass * speed_squared

    @property
    def rotational_kinetic_energy(self):
        return 0.5 * (
                self.Ixx * self.p ** 2 +
                self.Iyy * self.q ** 2 +
                self.Izz * self.r ** 2
        )

    @property
    def kinetic_energy(self):
        return self.translational_kinetic_energy + self.rotational_kinetic_energy

    @property
    def potential_energy(self):
        """
        Gives the potential energy [J] from gravity.

        PE = mgh
        """
        return self.mass * self.g * self.altitude

    def net_force(self, axes="body"):
        Fg_xb, Fg_yb, Fg_zb = self.convert_axes(0, 0, self.g, from_axes="earth", to_axes="body")

        F_xb = self.X + Fg_xb
        F_yb = self.Y + Fg_yb
        F_zb = self.Z + Fg_yb

        F_x_to, F_y_to, F_z_to = self.convert_axes(
            x_from=F_xb,
            y_from=F_yb,
            z_from=F_zb,
            from_axes="body",
            to_axes=axes
        )
        return F_x_to, F_y_to, F_z_to

    def d_translational_kinetic_energy(self):
        """
        Returns the derivative d(translational_kinetic_energy)/d(time) based on energy methods.
        """
        F_xb, F_yb, F_zb = self.net_force(axes="body")

        d_KE = (
                F_xb * self.u +
                F_yb * self.v +
                F_zb * self.w
        )
        return d_KE

    def d_speed(self):
        """
        Returns the derivative d(speed)/d(time) based on energy methods.
        """
        return self.d_translational_kinetic_energy() / (self.mass * self.speed)

    @property
    def altitude(self):
        return -self.ze

    @property
    def op_point(self):
        return OperatingPoint(
            atmosphere=Atmosphere(altitude=-self.ze),
            velocity=self.speed,
            alpha=self.alpha,
            beta=self.beta,
            p=self.p,
            q=self.q,
            r=self.r,
        )

    def convert_axes(self,
                     x_from, y_from, z_from,
                     from_axes: str,
                     to_axes: str,
                     ):
        """
        Converts a vector [x_from, y_from, z_from], as given in the `from_axes` frame, to an equivalent vector [x_to,
        y_to, z_to], as given in the `to_axes` frame.

        Identical to OperatingPoint.convert_axes(), but adds in "earth" as a valid axis frame. For more documentation,
        see the docstring of OperatingPoint.convert_axes().

        Both `from_axes` and `to_axes` should be a string, one of:
                * "geometry"
                * "body"
                * "wind"
                * "stability"
                * "earth"

        Args:
                x_from: x-component of the vector, in `from_axes` frame.
                y_from: y-component of the vector, in `from_axes` frame.
                z_from: z-component of the vector, in `from_axes` frame.
                from_axes: The axes to convert from.
                to_axes: The axes to convert to.

        Returns: The x-, y-, and z-components of the vector, in `to_axes` frame. Given as a tuple.

        """
        if from_axes == "earth" or to_axes == "earth":
            ### Trig Shorthands
            def sincos(x):
                try:
                    x = np.mod(x, 2 * np.pi)
                    one = np.ones_like(x)
                    zero = np.zeros_like(x)

                    if np.allclose(x, 0) or np.allclose(x, 2 * np.pi):
                        sin = zero
                        cos = one
                    elif np.allclose(x, np.pi / 2):
                        sin = one
                        cos = zero
                    elif np.allclose(x, np.pi):
                        sin = zero
                        cos = -one
                    elif np.allclose(x, 3 * np.pi / 2):
                        sin = -one
                        cos = zero
                    else:
                        raise ValueError()
                except:
                    sin = np.sin(x)
                    cos = np.cos(x)
                return sin, cos

                # Do the trig

            sphi, cphi = sincos(self.phi)
            sthe, cthe = sincos(self.theta)
            spsi, cpsi = sincos(self.psi)

        if from_axes == "earth":
            x_b = (
                    (cthe * cpsi) * x_from +
                    (cthe * spsi) * y_from +
                    (-sthe) * z_from
            )
            y_b = (
                    (sphi * sthe * cpsi - cphi * spsi) * x_from +
                    (sphi * sthe * spsi + cphi * cpsi) * y_from +
                    (sphi * cthe) * z_from
            )
            z_b = (
                    (cphi * sthe * cpsi + sphi * spsi) * x_from +
                    (cphi * sthe * spsi - sphi * cpsi) * y_from +
                    (cphi * cthe) * z_from
            )
        else:
            x_b, y_b, z_b = self.op_point.convert_axes(
                x_from, y_from, z_from,
                from_axes=from_axes, to_axes="body"
            )

        if to_axes == "earth":
            x_to = (
                    (cthe * cpsi) * x_b +
                    (sphi * sthe * cpsi - cphi * spsi) * y_b +
                    (cphi * sthe * cpsi + sphi * spsi) * z_b
            )
            y_to = (
                    (cthe * spsi) * x_b +
                    (sphi * sthe * spsi + cphi * cpsi) * y_b +
                    (cphi * sthe * spsi - sphi * cpsi) * z_b
            )
            z_to = (
                    (-sthe) * x_b +
                    (sphi * cthe) * y_b +
                    (cphi * cthe) * z_b
            )
        else:
            x_to, y_to, z_to = self.op_point.convert_axes(
                x_b, y_b, z_b,
                from_axes="body", to_axes=to_axes
            )

        return x_to, y_to, z_to


if __name__ == '__main__':
    import aerosandbox as asb

    opti = asb.Opti()

    n_timesteps = 300

    time = np.linspace(0, 1, n_timesteps)

    dyn = FreeBodyDynamics(
        opti_to_add_constraints_to=opti,
        time=time,
        xe=opti.variable(init_guess=np.linspace(0, 1, n_timesteps)),
        u=opti.variable(init_guess=1, n_vars=n_timesteps),
        X=opti.variable(init_guess=np.linspace(1, -1, n_timesteps)),
    )

    opti.subject_to([
        dyn.xe[0] == 0,
        dyn.xe[-1] == 1,
        dyn.u[0] == 0,
        dyn.u[-1] == 0,
    ])

    opti.minimize(
        np.sum(np.trapz(dyn.X ** 2) * np.diff(time))
    )

    sol = opti.solve()

    dyn.substitute_solution(sol)
