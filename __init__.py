import numpy as np
import os
import pickle
import matplotlib.pyplot as plt

class Crust1p0(object):
	"""docstring for Crust1p0"""
	def __init__(self, reread = False):
		if reread:
			create_dict()
		self.data = pickle.load(open('crust1p0.pkl', 'rb'))

	def gen_regional_map(self,m,min_lat,max_lat,min_lon,max_lon,
		cmap):
		min_lat = max(-89.5,np.floor(min_lat/0.5)*0.5)
		max_lat = min(89.5,np.ceil(max_lat/0.5)*0.5)
		min_lon = max(-179.5,np.floor(min_lon/0.5)*0.5)
		max_lon = min(179.5,np.ceil(max_lon/0.5)*0.5)
		lat = np.arange(min_lat,max_lat+1,1.0)
		lon = np.arange(min_lon,max_lon+1,1.0)
		lonXX,latYY = np.meshgrid(lon,lat)
		crustal_thick = np.zeros(np.shape(lonXX))
		for i in range(np.shape(lonXX)[0]):
			for j in range(np.shape(lonXX)[1]):
				bounds, Vp, Vs, Rho = self.point(latYY[i,j],lonXX[i,j])
				crustal_thick[i,j] = bounds[0]-bounds[-1]
		m.contourf(lonXX,latYY, crustal_thick,cmap=cmap)
		m.colorbar(location='right')

	def gen_global_map(self,m,cmap):
		self.gen_regional_map(m,-89.5,89.5,-179.5,179.5,cmap)

	def plot_crust_at_point(self,ax,lat,lon):
		bounds, Vp, Vs, Rho = self.point(lat,lon)
		colors = ['b','c','gold','orange','darkorange','lightcoral','coral','red','brown']
		legends = ['water','ice','upper sediments','middle sediments',\
		'lower sediments','upper crystalline crust','middle crystalline crust',\
		'lower crystalline crust', 'mantle']
		str_fmt = 'v_s = {0:7.2f} km, v_p = {1:7.2f} km, v_s = {2:7.2f} tons/m^3'
		for i,bound in enumerate(bounds):
			ax.axhline(bound,0,100, c='k', lw=0.5)
			if i == (len(bounds)-1):
				ax.fill_between([0.0,100.0],bound,bound-10,\
					color=colors[i],label=legends[i])
				thick = True
			else:
				ax.fill_between([0.0,100.0],bound,bounds[i+1],\
					color=colors[i],label=legends[i])
				if abs(bound - bounds[i+1])>0.0:
					thick = True
				else:
					thick = False
			if thick:
				string = str_fmt.format(Vs[i],Vp[i],Rho[i])
				ax.text(50.0,bound,string,ha='center',va='top')
		ax.set_yticks(ticks=bounds)
		ax.set_ylabel('depth (km)')
		ax.set_title('Crustal Layer at Lat {0:5.2f} Lon {1:5.2f}'.format(lat,lon))
		ax.legend()

	def point(self, lat, lon, string = False):
		j = int(lon+179.5)
		i = int(89.5-lat)
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

def read_db(dir='./data/'):
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
	'''
	import matplotlib.pyplot as plt
	if not(os.path.isfile('crust1p0.pkl')):
		read_db(dir='./../data/')
	else:
		read_db(dir='./../data/')
	c = Crust1p0()
	fig, ax = plt.subplots()
	c.plot_crust_at_point(ax,73.5,23.5)
	plt.show()
	'''
	from mpl_toolkits.basemap import Basemap
	import matplotlib.pyplot as plt
	import numpy as np
	import matplotlib.cm as cm
	fig = plt.figure(figsize=(30,20))
	m = Basemap(width=800000000,height=700000000)
	m.drawparallels(np.arange(-90,90,20),labels=[True])
	m.drawmeridians(np.arange(-180,180,20),labels=[False,True,True,False], rotation=90)
	m.drawcountries()
	m.drawcoastlines()
	m.drawstates()
	c = Crust1p0()
	c.gen_global_map(m,plt.cm.jet)
	plt.savefig('sample.pdf')