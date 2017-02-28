clear all; clc
%===========================================E0
Einfo1 = hdf5info('ex-000200.00.h5');
E1 = hdf5read(Einfo1.GroupHierarchy.Datasets(1));
E2 = hdf5read(Einfo1.GroupHierarchy.Datasets(2));
E_slice1(:,:) = E1(:,:,50);
E_slice2(:,:) = E2(:,:,50);
X = abs(E_slice1).^2;
Y = abs(E_slice2).^2;
Ex = X+Y;
Einfo2 = hdf5info('ey-000200.00.h5');
E3 = hdf5read(Einfo2.GroupHierarchy.Datasets(1));
E4 = hdf5read(Einfo2.GroupHierarchy.Datasets(2));
E_slice3(:,:) = E3(:,:,50);
E_slice4(:,:) = E4(:,:,50);
x = abs(E_slice3).^2;
y = abs(E_slice4).^2;
Ey = x+y;
Einfo3 = hdf5info('ez-000200.00.h5');
E5 = hdf5read(Einfo3.GroupHierarchy.Datasets(1));
E6 = hdf5read(Einfo3.GroupHierarchy.Datasets(2));
E_slice5(:,:) = E5(:,:,50);
E_slice6(:,:) = E6(:,:,50);
a = abs(E_slice5).^2;
b = abs(E_slice6).^2;
Ez = a+b;
normE50 = sqrt(Ex+Ey+Ez);
plane50 = normE50(35:49,95:126);
E50 = mean(plane50(:));
%===========================================E1
e_slice1(:,:) = E1(:,:,450);
e_slice2(:,:) = E2(:,:,450);
X1 = abs(e_slice1).^2;
Y1 = abs(e_slice2).^2;
ex = X1+Y1;
e_slice3(:,:) = E3(:,:,450);
e_slice4(:,:) = E4(:,:,450);
x1 = abs(e_slice3).^2;
y1 = abs(e_slice4).^2;
ey = x1+y1;
e_slice5(:,:) = E5(:,:,450);
e_slice6(:,:) = E6(:,:,450);
a1 = abs(e_slice5).^2;
b1 = abs(e_slice6).^2;
ez = a1+b1;
normE450 = sqrt(ex+ey+ez);
plane450 = normE450(35:49,95:126);
E450 = mean(plane450(:));

Loss = -1/9*log(E450^2/E50^2);
disp(Loss);



