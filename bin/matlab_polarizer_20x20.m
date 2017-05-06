clear;clc;
% Ey transmission
Einfo = hdf5info('ey-000001000.h5');
E1 = hdf5read(Einfo.GroupHierarchy.Datasets(1));
E2 = hdf5read(Einfo.GroupHierarchy.Datasets(2));
Ey = abs(E1*1i+E2).^2;
E_slice(:,:) = Ey(:,:,19);
eyt = mean(E_slice(:));

%Ex transmission
einfo = hdf5info('ex-000001000.h5');
e1 = hdf5read(einfo.GroupHierarchy.Datasets(1));
e2 = hdf5read(einfo.GroupHierarchy.Datasets(2));
ey = abs(e1*1i+e2).^2;
E_slice1(:,:) = ey(:,:,100);
ext = mean(E_slice1(:));

%Transmission
T = ext/eyt;

fileID = fopen('../results.txt', 'w')
fprintf(fileID, '%f', T)
