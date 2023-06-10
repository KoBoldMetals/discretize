import numpy as np
import unittest
import discretize


class TestInnerProducts(discretize.tests.OrderTest):
    """Integrate an function over a unit cube domain
    using edgeInnerProducts and faceInnerProducts."""

    meshTypes = ["uniformTensorMesh", "uniformCurv", "rotateCurv"]
    meshDimension = 3
    meshSizes = [16, 32]

    def getError(self):
        call = lambda fun, xyz: fun(xyz[:, 0], xyz[:, 1], xyz[:, 2])

        ex = lambda x, y, z: x**2 + y * z
        ey = lambda x, y, z: (z**2) * x + y * z
        ez = lambda x, y, z: y**2 + x * z

        sigma1 = lambda x, y, z: x * y + 1
        sigma2 = lambda x, y, z: x * z + 2
        sigma3 = lambda x, y, z: 3 + z * y
        sigma4 = lambda x, y, z: 0.1 * x * y * z
        sigma5 = lambda x, y, z: 0.2 * x * y
        sigma6 = lambda x, y, z: 0.1 * z

        Gc = self.M.gridCC
        if self.sigmaTest == 1:
            sigma = np.c_[call(sigma1, Gc)]
            analytic = 647.0 / 360  # Found using sympy.
        elif self.sigmaTest == 3:
            sigma = np.r_[call(sigma1, Gc), call(sigma2, Gc), call(sigma3, Gc)]
            analytic = 37.0 / 12  # Found using sympy.
        elif self.sigmaTest == 6:
            sigma = np.c_[
                call(sigma1, Gc),
                call(sigma2, Gc),
                call(sigma3, Gc),
                call(sigma4, Gc),
                call(sigma5, Gc),
                call(sigma6, Gc),
            ]
            analytic = 69881.0 / 21600  # Found using sympy.

        if self.location == "edges":
            cart = lambda g: np.c_[call(ex, g), call(ey, g), call(ez, g)]
            Ec = np.vstack(
                (cart(self.M.gridEx), cart(self.M.gridEy), cart(self.M.gridEz))
            )
            E = self.M.project_edge_vector(Ec)

            if self.invert_model:
                A = self.M.get_edge_inner_product(
                    discretize.utils.inverse_property_tensor(self.M, sigma),
                    invert_model=True,
                )
            else:
                A = self.M.get_edge_inner_product(sigma)
            numeric = E.T.dot(A.dot(E))
        elif self.location == "faces":
            cart = lambda g: np.c_[call(ex, g), call(ey, g), call(ez, g)]
            Fc = np.vstack(
                (cart(self.M.gridFx), cart(self.M.gridFy), cart(self.M.gridFz))
            )
            F = self.M.project_face_vector(Fc)

            if self.invert_model:
                A = self.M.get_face_inner_product(
                    discretize.utils.inverse_property_tensor(self.M, sigma),
                    invert_model=True,
                )
            else:
                A = self.M.get_face_inner_product(sigma)
            numeric = F.T.dot(A.dot(F))

        err = np.abs(numeric - analytic)
        return err

    def test_order1_edges(self):
        self.name = "Edge Inner Product - Isotropic"
        self.location = "edges"
        self.sigmaTest = 1
        self.invert_model = False
        self.orderTest()

    def test_order1_edges_invert_model(self):
        self.name = "Edge Inner Product - Isotropic - invert_model"
        self.location = "edges"
        self.sigmaTest = 1
        self.invert_model = True
        self.orderTest()

    def test_order3_edges(self):
        self.name = "Edge Inner Product - Anisotropic"
        self.location = "edges"
        self.sigmaTest = 3
        self.invert_model = False
        self.orderTest()

    def test_order3_edges_invert_model(self):
        self.name = "Edge Inner Product - Anisotropic - invert_model"
        self.location = "edges"
        self.sigmaTest = 3
        self.invert_model = True
        self.orderTest()

    def test_order6_edges(self):
        self.name = "Edge Inner Product - Full Tensor"
        self.location = "edges"
        self.sigmaTest = 6
        self.invert_model = False
        self.orderTest()

    def test_order6_edges_invert_model(self):
        self.name = "Edge Inner Product - Full Tensor - invert_model"
        self.location = "edges"
        self.sigmaTest = 6
        self.invert_model = True
        self.orderTest()

    def test_order1_faces(self):
        self.name = "Face Inner Product - Isotropic"
        self.location = "faces"
        self.sigmaTest = 1
        self.invert_model = False
        self.orderTest()

    def test_order1_faces_invert_model(self):
        self.name = "Face Inner Product - Isotropic - invert_model"
        self.location = "faces"
        self.sigmaTest = 1
        self.invert_model = True
        self.orderTest()

    def test_order3_faces(self):
        self.name = "Face Inner Product - Anisotropic"
        self.location = "faces"
        self.sigmaTest = 3
        self.invert_model = False
        self.orderTest()

    def test_order3_faces_invert_model(self):
        self.name = "Face Inner Product - Anisotropic - invert_model"
        self.location = "faces"
        self.sigmaTest = 3
        self.invert_model = True
        self.orderTest()

    def test_order6_faces(self):
        self.name = "Face Inner Product - Full Tensor"
        self.location = "faces"
        self.sigmaTest = 6
        self.invert_model = False
        self.orderTest()

    def test_order6_faces_invert_model(self):
        self.name = "Face Inner Product - Full Tensor - invert_model"
        self.location = "faces"
        self.sigmaTest = 6
        self.invert_model = True
        self.orderTest()


class TestInnerProducts2D(discretize.tests.OrderTest):
    """Integrate an function over a unit cube domain
    using edgeInnerProducts and faceInnerProducts."""

    meshTypes = ["uniformTensorMesh", "uniformCurv", "rotateCurv"]
    meshDimension = 2
    meshSizes = [4, 8, 16, 32, 64, 128]

    def getError(self):
        z = 5  # Because 5 is just such a great number.

        call = lambda fun, xy: fun(xy[:, 0], xy[:, 1])

        ex = lambda x, y: x**2 + y * z
        ey = lambda x, y: (z**2) * x + y * z

        sigma1 = lambda x, y: x * y + 1
        sigma2 = lambda x, y: x * z + 2
        sigma3 = lambda x, y: 3 + z * y

        Gc = self.M.gridCC
        if self.sigmaTest == 1:
            sigma = np.c_[call(sigma1, Gc)]
            analytic = 144877.0 / 360  # Found using sympy. z=5
        elif self.sigmaTest == 2:
            sigma = np.c_[call(sigma1, Gc), call(sigma2, Gc)]
            analytic = 189959.0 / 120  # Found using sympy. z=5
        elif self.sigmaTest == 3:
            sigma = np.r_[call(sigma1, Gc), call(sigma2, Gc), call(sigma3, Gc)]
            analytic = 781427.0 / 360  # Found using sympy. z=5

        if self.location == "edges":
            cart = lambda g: np.c_[call(ex, g), call(ey, g)]
            Ec = np.vstack((cart(self.M.gridEx), cart(self.M.gridEy)))
            E = self.M.project_edge_vector(Ec)
            if self.invert_model:
                A = self.M.get_edge_inner_product(
                    discretize.utils.inverse_property_tensor(self.M, sigma),
                    invert_model=True,
                )
            else:
                A = self.M.get_edge_inner_product(sigma)
            numeric = E.T.dot(A.dot(E))
        elif self.location == "faces":
            cart = lambda g: np.c_[call(ex, g), call(ey, g)]
            Fc = np.vstack((cart(self.M.gridFx), cart(self.M.gridFy)))
            F = self.M.project_face_vector(Fc)

            if self.invert_model:
                A = self.M.get_face_inner_product(
                    discretize.utils.inverse_property_tensor(self.M, sigma),
                    invert_model=True,
                )
            else:
                A = self.M.get_face_inner_product(sigma)
            numeric = F.T.dot(A.dot(F))

        err = np.abs(numeric - analytic)
        return err

    def test_order1_edges(self):
        self.name = "2D Edge Inner Product - Isotropic"
        self.location = "edges"
        self.sigmaTest = 1
        self.invert_model = False
        self.orderTest()

    def test_order1_edges_invert_model(self):
        self.name = "2D Edge Inner Product - Isotropic - invert_model"
        self.location = "edges"
        self.sigmaTest = 1
        self.invert_model = True
        self.orderTest()

    def test_order3_edges(self):
        self.name = "2D Edge Inner Product - Anisotropic"
        self.location = "edges"
        self.sigmaTest = 2
        self.invert_model = False
        self.orderTest()

    def test_order3_edges_invert_model(self):
        self.name = "2D Edge Inner Product - Anisotropic - invert_model"
        self.location = "edges"
        self.sigmaTest = 2
        self.invert_model = True
        self.orderTest()

    def test_order6_edges(self):
        self.name = "2D Edge Inner Product - Full Tensor"
        self.location = "edges"
        self.sigmaTest = 3
        self.invert_model = False
        self.orderTest()

    def test_order6_edges_invert_model(self):
        self.name = "2D Edge Inner Product - Full Tensor - invert_model"
        self.location = "edges"
        self.sigmaTest = 3
        self.invert_model = True
        self.orderTest()

    def test_order1_faces(self):
        self.name = "2D Face Inner Product - Isotropic"
        self.location = "faces"
        self.sigmaTest = 1
        self.invert_model = False
        self.orderTest()

    def test_order1_faces_invert_model(self):
        self.name = "2D Face Inner Product - Isotropic - invert_model"
        self.location = "faces"
        self.sigmaTest = 1
        self.invert_model = True
        self.orderTest()

    def test_order2_faces(self):
        self.name = "2D Face Inner Product - Anisotropic"
        self.location = "faces"
        self.sigmaTest = 2
        self.invert_model = False
        self.orderTest()

    def test_order2_faces_invert_model(self):
        self.name = "2D Face Inner Product - Anisotropic - invert_model"
        self.location = "faces"
        self.sigmaTest = 2
        self.invert_model = True
        self.orderTest()

    def test_order3_faces(self):
        self.name = "2D Face Inner Product - Full Tensor"
        self.location = "faces"
        self.sigmaTest = 3
        self.invert_model = False
        self.orderTest()

    def test_order3_faces_invert_model(self):
        self.name = "2D Face Inner Product - Full Tensor - invert_model"
        self.location = "faces"
        self.sigmaTest = 3
        self.invert_model = True
        self.orderTest()


class TestInnerProducts1D(discretize.tests.OrderTest):
    """Integrate an function over a unit cube domain
    using edgeInnerProducts and faceInnerProducts."""

    meshTypes = ["uniformTensorMesh"]
    meshDimension = 1
    meshSizes = [4, 8, 16, 32, 64, 128]

    def getError(self):
        y = 12  # Because 12 is just such a great number.
        z = 5  # Because 5 is just such a great number as well!

        call = lambda fun, x: fun(x)

        ex = lambda x: x**2 + y * z

        sigma1 = lambda x: x * y + 1

        Gc = self.M.gridCC
        sigma = call(sigma1, Gc)
        analytic = 128011.0 / 5  # Found using sympy. y=12, z=5

        if self.location == "faces":
            F = call(ex, self.M.gridFx)
            if self.invert_model:
                A = self.M.get_face_inner_product(1 / sigma, invert_model=True)
            else:
                A = self.M.get_face_inner_product(sigma)
            numeric = F.T.dot(A.dot(F))

        err = np.abs(numeric - analytic)
        return err

    def test_order1_faces(self):
        self.name = "1D Face Inner Product"
        self.location = "faces"
        self.sigmaTest = 1
        self.invert_model = False
        self.orderTest()

    def test_order1_faces_invert_model(self):
        self.name = "1D Face Inner Product - invert_model"
        self.location = "faces"
        self.sigmaTest = 1
        self.invert_model = True
        self.orderTest()


if __name__ == "__main__":
    unittest.main()

###################################################
#### Uncomment to Reevaluate the InnerProducts ####
###################################################

# if __name__ == '__main__':
# import sympy

# x,y,z = sympy.symbols(['x','y','z'])
# ex = x**2+y*z
# ey = (z**2)*x+y*z
# ez = y**2+x*z
# e = sympy.Matrix([ex,ey,ez])

# sigma1 = x*y+1
# sigma2 = x*z+2
# sigma3 = 3+z*y
# sigma4 = 0.1*x*y*z
# sigma5 = 0.2*x*y
# sigma6 = 0.1*z

# S1 = sympy.Matrix([[sigma1,0,0],[0,sigma1,0],[0,0,sigma1]])
# S2 = sympy.Matrix([[sigma1,0,0],[0,sigma2,0],[0,0,sigma3]])
# S3 = sympy.Matrix([[sigma1,sigma4,sigma5],[sigma4,sigma2,sigma6],[sigma5,sigma6,sigma3]])

# print('3D')
# print(sympy.integrate(sympy.integrate(sympy.integrate(e.T*S1*e, (x,0,1)), (y,0,1)), (z,0,1)))
# print(sympy.integrate(sympy.integrate(sympy.integrate(e.T*S2*e, (x,0,1)), (y,0,1)), (z,0,1)))
# print(sympy.integrate(sympy.integrate(sympy.integrate(e.T*S3*e, (x,0,1)), (y,0,1)), (z,0,1)))


# z = 5
# ex = x**2+y*z
# ey = (z**2)*x+y*z
# e = sympy.Matrix([ex,ey])

# sigma1 = x*y+1
# sigma2 = x*z+2
# sigma3 = 3+z*y

# S1 = sympy.Matrix([[sigma1,0],[0,sigma1]])
# S2 = sympy.Matrix([[sigma1,0],[0,sigma2]])
# S3 = sympy.Matrix([[sigma1,sigma3],[sigma3,sigma2]])

# print('2D')
# print(sympy.integrate(sympy.integrate(e.T*S1*e, (x,0,1)), (y,0,1)))
# print(sympy.integrate(sympy.integrate(e.T*S2*e, (x,0,1)), (y,0,1)))
# print(sympy.integrate(sympy.integrate(e.T*S3*e, (x,0,1)), (y,0,1)))

# y = 12
# z = 5
# ex = x**2+y*z
# e = ex

# sigma1 = x*y+1

# print('1D')
# print(sympy.integrate(e*sigma1*e, (x,0,1)))
