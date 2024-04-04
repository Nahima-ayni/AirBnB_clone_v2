# Puppet manifest to set up web servers for the deployment of web_static

# Ensure the package manager is updated and nginx is installed
package { 'nginx':
  ensure => installed,
  before => File['/etc/nginx/sites-enabled/default'],
}

# Allow Nginx HTTP through the firewall
firewall { '100 allow nginx http':
  action => 'accept',
  proto  => 'tcp',
  port   => '80',
}

# Create directories for web_static
file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create a test index.html file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => '<html><head><title>Test Page</title></head><body>This is a test page</body></html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Remove current symlink and create a new one
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force  => true,
  require => File['/data/web_static/releases/test/index.html'],
}

# Update nginx configuration to serve the static content
file_line { 'nginx_site_config':
  path => '/etc/nginx/sites-enabled/default',
  line => '    location /hbnb_static { alias /data/web_static/current/; }',
  match => '^\\s*listen 80 default_server;',
  append_on_no_match => true,
  notify => Service['nginx'],
}

# Ensure nginx service is running
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-enabled/default'],
}
