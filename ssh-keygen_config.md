# Add SSH-KEY to avoid asking for password.

### Instruction:

1. Install Git for Windows
2. Open Git bash
3. run command "ssh-keygen -o -t -b 4096 -C "your@email" 
4. Just press enter for default
5. Once generated, copy the key in id_rsa.pub and paste in github profile --> setting -- > ssh-keys.
6. Test the config "ssh -T git@git.lisnepal.com.np".
