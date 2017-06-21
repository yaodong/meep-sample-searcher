clear;clc;
% Ez transmission
Einfo = hdf5info('ez-000001000.h5');
E1 = hdf5read(Einfo.GroupHierarchy.Datasets(1));
E2 = hdf5read(Einfo.GroupHierarchy.Datasets(2));
Ez = abs(E1*1i+E2).^2;
E_slice(:,:) = Ez(:,:,100);
ezt = mean(E_slice(:));

%Ey transmission
einfo = hdf5info('ey-000001000.h5');
e1 = hdf5read(einfo.GroupHierarchy.Datasets(1));
e2 = hdf5read(einfo.GroupHierarchy.Datasets(2));
Ey = abs(e1*1i+e2).^2;
E_slice1(:,:) = Ey(:,:,100);
eyt = mean(E_slice1(:));

%Ex transmission
EInfo = hdf5info('ex-000001000.h5');
e_1 = hdf5read(EInfo.GroupHierarchy.Datasets(1));
e_2 = hdf5read(EInfo.GroupHierarchy.Datasets(2));
Ex = abs(e_1*1i+e_2).^2;
E_slice2(:,:) = Ex(:,:,100);
ext = mean(E_slice2(:));

%Transmission
T = [eyt, ezt, ext];

fileID = fopen('../results.csv', 'w')
fprintf(fileID, 'eyt:%f,ezt:%f,ext:%f', T)
