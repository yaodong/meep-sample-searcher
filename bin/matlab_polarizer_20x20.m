clear;clc;
% Ez transmission
Einfo = hdf5info('ez-000001000.h5');
E1 = hdf5read(Einfo.GroupHierarchy.Datasets(1));
E2 = hdf5read(Einfo.GroupHierarchy.Datasets(2));
Ez = abs(E1*1i+E2).^2;
E_slice(:,:) = Ez(:,:,10);
ezt = mean(E_slice(:));

%Ey transmission
einfo = hdf5info('ey-000001000.h5');
e1 = hdf5read(einfo.GroupHierarchy.Datasets(1));
e2 = hdf5read(einfo.GroupHierarchy.Datasets(2));
Ey = abs(e1*1i+e2).^2;
E_slice1(:,:) = Ey(:,:,100);
eyt = mean(E_slice1(:));

%Transmission
T = eyt/ezt;

fileID = fopen('../results.txt', 'w')
fprintf(fileID, '%f', T)

