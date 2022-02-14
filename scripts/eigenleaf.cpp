#include <iostream>
#include <libraries/Eigen/Dense>
#include <libraries/Spectra/GenEigsSolver.h>
#include <libraries/Spectra/MatOp/DenseGenMatProd.h>
 
using Eigen::MatrixXd;
using Eigen::VectorXd;
using Eigen::VectorXcd;
using namespace Spectra;
using namespace std;

int main()
{
  // ====== Generate covariance matrix ======
  // Get data.
  MatrixXd m(5,3);
  m << 90.0, 60.0, 90.0, 
       90.0, 90.0, 30.0, 
       60.0, 60.0, 60.0, 
       60.0, 60.0, 90.0, 
       30.0, 30.0, 30.0;

  //Get matrix 1: x = X - 1.1'X(1/n)
  m = m - MatrixXd::Constant(5,5,1)*(m*0.2);
  //Get matrix 2: V = x'x(1/n)
  m = (m.transpose()*m)*0.2;

  cout << "Covariance Matrix" << endl;
  cout << m << endl;

  // ====== Get eigen-things ======
  // Get eigenvalues (from Spectra documentation)
  // DenseGenMatProd<double> op(m);
  // GenEigsSolver<DenseGenMatProd<double>> eigs(op, 1, 3);
  
  // eigs.init();
  // int nconv = eigs.compute(SortRule::LargestMagn);
  
  // VectorXcd evalues;
  // if (eigs.info() == CompInfo::Successful)
  //   evalues = eigs.eigenvalues();
  
  // std::cout << "Eigenvalues found:\n" << evalues << std::endl;

  // Get eigenvectors from value. 0 = (m - lambda)x

  Eigen::EigenSolver<Eigen::MatrixXd> eigensolver;
  eigensolver.compute(m);
  
  // Eigen::VectorXd eigen_values = eigensolver.eigenvalues().real();
  // std::cout << eigen_values << std::endl;

  Eigen::MatrixXd eigen_vectors = eigensolver.eigenvectors().real();
  std::cout << eigen_vectors << std::endl;

  return 0;
}