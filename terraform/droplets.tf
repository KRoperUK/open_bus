resource "digitalocean_droplet" "web" {
    backups              = false
    image                = "ubuntu-23-10-x64"
    ipv6                 = false
    monitoring           = true
    name                 = "open-bus"
    region               = "fra1"
    resize_disk          = true
    size                 = "s-1vcpu-512mb-10gb"
    tags                 = [
        "open-bus",
    ]
    volume_ids           = []
}