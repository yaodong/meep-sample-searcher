Einfo = hdf5info('ex-000300.00.h5');
E = hdf5read(Einfo.GroupHierarchy.Datasets);
E_slice(:,:) = E(:,:,100);
Ex = abs(E_slice).^2;
ex = mean(Ex(:));
plane = Ex(25:525,25:525);
ex = mean(plane(:));
