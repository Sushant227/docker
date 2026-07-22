# Creating EFS + Mount Target via AWS Console, Then Using as a Docker Volume on EC2

## Part 1: Create the EFS File System (Console)

1. Go to the **AWS Console** → search for **"EFS"** → open **Elastic File System**.
2. Click **Create file system**.
3. You'll see a quick-create screen:
   - **Name**: e.g., `my-app-efs`
   - **VPC**: select the **same VPC** your EC2 instance is in (this is critical)
   - Leave everything else default for now (you can click "Customize" if you want to control settings below)
4. Click **Create**.

### If you click "Customize" instead (recommended for production):
- **Availability and durability**: choose *Regional* (multi-AZ, default) or *One Zone* (cheaper, single AZ — only if your EC2 is in one AZ)
- **Throughput mode**: Bursting (default, fine for most use cases) or Provisioned
- **Encryption**: leave "Enable encryption of data at rest" checked (recommended)
- Click **Next**

### Network settings (this is where mount targets get created)
- You'll see a table listing every AZ in your VPC
- For each AZ where you have EC2 instances, make sure:
  - **Subnet** is selected (pick the subnet your EC2 instance lives in)
  - **Security group** — this is important, see Part 2 below
- Click **Next** → **Next** (skip file system policy unless you need one) → **Create**

This single step in the console does what Steps 1 + 5 did via CLI — it creates the file system **and** the mount targets together, per AZ.

## Part 2: Configure Security Groups (Console)

Before or right after creating EFS, set up the security group rule:

1. Go to **EC2 Console** → **Security Groups** (left sidebar)
2. Find your **EC2 instance's security group** — note its ID (e.g., `sg-0abc123`)
3. Now find (or create) the **security group used by your EFS mount targets**:
   - If you let EFS create a default one during setup, find it (usually named after your VPC)
   - Click on it → **Inbound rules** tab → **Edit inbound rules**
4. Click **Add rule**:
   - **Type**: NFS
   - **Port range**: 2049 (auto-fills when you pick NFS)
   - **Source**: select **Custom**, then pick your **EC2 instance's security group** from the dropdown
5. Click **Save rules**

> If you already selected your EC2's security group directly as the mount target's SG during EFS creation (Part 1), you can skip creating a separate rule — but usually AWS creates its own default SG for EFS, so this step is still needed.

## Part 3: Verify Mount Targets Are Ready

1. In the **EFS Console**, click into your file system
2. Go to the **Network** tab
3. Confirm each AZ shows a mount target with **Lifecycle State: Available** (may take ~1 minute after creation)

## Part 4: Get the Mount Command from the Console

1. Still in your file system's page, click **Attach** (top right button)
2. AWS gives you three ready-made mount commands:
   - Using the EFS mount helper (`mount -t efs ...`)
   - Using NFS client directly (`mount -t nfs4 ...`)
   - A **DNS name** you can copy: `fs-0123456789abcdef0.efs.us-east-1.amazonaws.com`
3. Copy the NFS command shown — it'll look like:
```bash
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport \
  fs-0123456789abcdef0.efs.us-east-1.amazonaws.com:/ /mnt/efs
```

## Part 5: On Your EC2 Instance — Install NFS Client and Mount

SSH into your EC2 instance (via Console's **Connect** button or your terminal):

```bash
# Amazon Linux 2/2023
sudo yum install -y amazon-efs-utils

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y nfs-common
```

Create the mount point and mount:

```bash
sudo mkdir -p /mnt/efs

sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport \
  fs-0123456789abcdef0.efs.us-east-1.amazonaws.com:/ /mnt/efs
```

Verify:
```bash
df -h /mnt/efs
echo "test" | sudo tee /mnt/efs/hello.txt
```

## Part 6: Make It Persistent (survive reboot)

```bash
echo "fs-0123456789abcdef0.efs.us-east-1.amazonaws.com:/ /mnt/efs nfs4 _netdev,nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport 0 0" | sudo tee -a /etc/fstab

# test it survives
sudo umount /mnt/efs
sudo mount -a
df -h /mnt/efs
```

## Part 7: Use It as a Docker Volume

Now that `/mnt/efs` is a working mount on the EC2 host, just bind-mount it into your container:

```bash
docker run -d \
  --name my_app \
  -v /mnt/efs:/data \
  my_app_image
```

Or with Docker Compose:
```yaml
services:
  app:
    image: my_app_image
    volumes:
      - /mnt/efs:/data
```

Everything the container writes to `/data` is actually stored on EFS — persistent, and shareable with any other EC2 instance/container that mounts the same file system.

---

## Quick recap of the console flow

```
EFS Console → Create file system (pick same VPC, subnets per AZ)
        ↓
EC2 Console → Security Groups → allow port 2049 from EC2's SG
        ↓
EFS Console → check Network tab → mount targets "Available"
        ↓
EFS Console → click "Attach" → copy mount command
        ↓
SSH into EC2 → install nfs-common/efs-utils → mkdir + mount
        ↓
Add to /etc/fstab for persistence
        ↓
docker run -v /mnt/efs:/data your_image
```

Want a screenshot-by-screenshot walkthrough of any specific console screen (e.g., the Network settings tab during EFS creation, since that's where AZ/subnet/security-group mistakes usually happen)?
