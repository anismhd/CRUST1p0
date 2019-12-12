import numpy as np
import os
import pickle

class Crust1p0(object):
	"""docstring for Crust1p0"""
	def __init__(self, reread = False):
		if reread:
			create_dict()
		self.data = pickle.load(open('crust1p0.pkl', 'rb'))

	def write_xyz(self):
		for i in range(180):
			lat = 89.0 - i + 0.5
			for j in range(360):
				lon = -179 + j -0.5
				print(lon,lat,self.data['Bounds'][i,j,0])

	def point(self, lat, lon, string = False):
		j = int(lon+180)
		i = int(89.5-)
		print(i,j)
		if string == True:
			fmt = '{0:12.3f} {1:10.3f} {2:10.3f} {3:10.3f}\n'
			strr = '{0:34}={1:10.3f}\n'.format(\
				'Surface elevation',self.data['Bounds'][i,j,0])
			strr = strr + '{0:>12s} {1:>10s} {2:>10s} {3:>10s}\n'.format(\
				'Bottom Dpt.','Vp','Vs','Density')
			for k in range(1,9):
				strr = strr + fmt.format(\
					self.data['Bounds'][i,j][k],\
					self.data['Vp'][i,j][k-1],\
					self.data['Vs'][i,j][k-1],\
					self.data['Rho'][i,j][k-1])
			strr = strr + '{0:12s} {1:10.3f} {2:10.3f} {3:10.3f}\n'.format(\
				'Mantle',self.data['Vp'][i,j,-1],self.data['Vs'][i,j,-1],self.data['Rho'][i,j,-1])
			return strr
		else:
			return self.data['Bounds'][i,j,:],self.data['Vp'][i,j,:],self.data['Vs'][i,j,:],self.data['Rho'][i,j,:]


	def get_map(self,lc_lat,lc_lon,tc_lat,tc_lon, output='crustal_thickness'):
		data = self.map(lc_lat,lc_lon,tc_lat,tc_lon)

	def map(self,lc_lat,lc_lon,tc_lat,tc_lon):
		if (lc_lon <= -179.5):
			lb_j = 0
			lon_min = -179.5
		else:
			lb_j = int(lc_lon+180)-1
			lon_min = -179.5 + lb_j
		if (tc_lon >= 179.5):
			ub_j = 360
			lon_max = 179.5
		else:
			ub_j = int(tc_lon+180)+1
			lon_max = -179.5 + ub_j
		if (lc_lat <= -89.5):
			lb_i = 0
			lat_min = 89.5
		else:
			lb_i = int(lc_lat+90)-1
			lat_min = -89.5 + lb_i
		if (tc_lat >= 89.5):
			ub_i = 180
			lat_max = 89.5
		else:
			ub_i = int(tc_lat+90)+1
			lat_max = -89.5 + ub_i
		data = {}
		lat_list = np.arange(lat_min,lat_max+1,1)
		lon_list = np.arange(lon_min,lon_max+1,1)
		XX,YY = np.meshgrid(lon_list,lat_list)
		data['latlon_grid'] = [XX,YY]
		ln_i = np.size(XX,0)
		ln_j = np.size(XX,1)
		data['depth2base'] = np.zeros([ln_i,ln_j,9])
		data['Vp'] = np.zeros([ln_i,ln_j,9])
		data['Vs'] = np.zeros([ln_i,ln_j,9])
		data['Rho'] = np.zeros([ln_i,ln_j,9])
		for i,lat in enumerate(lat_list):
			for j,lon in enumerate(lon_list):
				bounds, Vp, Vs, Rho = self.point(lat,lon)
				data['depth2base'][i,j,:] = bounds
				data['Vp'][i,j,:] = Vp
				data['Vs'][i,j,:] = Vs
				data['Rho'][i,j,:] = Rho
		return data
def read_db(dir='./'):
	VpID = open(dir+'crust1.vp','r')
	VsID = open(dir+'crust1.vs','r')
	RhID = open(dir+'crust1.rho','r')
	BdID = open(dir+'crust1.bnds', 'r')
	CRUST1p0 = {'gridDataLat':np.zeros([180,360]),\
				'gridDataLon':np.zeros([180,360]),\
				'Vp':np.zeros([180,360,9]),\
				'Vs':np.zeros([180,360,9]),\
				'Bounds':np.zeros([180,360,9]),\
				'Rho':np.zeros([180,360,9])}
	for i in range(180):
		lat = 89.0 - i + 0.5
		for j in range(360):
			lon = -179 + j -0.5
			CRUST1p0['gridDataLat'][i,j] = lat
			CRUST1p0['gridDataLon'][i,j] = lon
			CRUST1p0['Vp'][i,j,:] = np.array([float(val) for val in VpID.readline().strip().split()])
			CRUST1p0['Vs'][i,j,:] = np.array([float(val) for val in VsID.readline().strip().split()])
			CRUST1p0['Rho'][i,j,:] = np.array([float(val) for val in RhID.readline().strip().split()])
			CRUST1p0['Bounds'][i,j,:] = np.array([float(val) for val in BdID.readline().strip().split()])
	VpID.close()
	VsID.close()
	RhID.close()
	BdID.close()
	pickle.dump(CRUST1p0,open('crust1p0.pkl', 'wb'))
if __name__ == '__main__':
	if not(os.path.isfile('crust1p0.pkl')):
		read_db(dir='/media/sf_E_DRIVE/VB_FOLDERS/BitBucket/CRUST1p0/data/')
	else:
		read_db(dir='/media/sf_E_DRIVE/VB_FOLDERS/BitBucket/CRUST1p0/data/')
	c = Crust1p0()
	print(c.point(74.5,22.5, string=True))