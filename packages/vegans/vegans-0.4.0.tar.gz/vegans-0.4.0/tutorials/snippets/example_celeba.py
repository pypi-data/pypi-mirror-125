import torch

import numpy as np
import matplotlib.pyplot as plt
import vegans.utils as utils
import vegans.utils.loading as loading

from vegans.GAN import (
    ConditionalAAE,
    ConditionalBicycleGAN,
    ConditionalEBGAN,
    ConditionalKLGAN,
    ConditionalLRGAN,
    ConditionalLSGAN,
    ConditionalPix2Pix,
    ConditionalVAEGAN,
    ConditionalVanillaGAN,
    ConditionalVanillaVAE,
    ConditionalWassersteinGAN,
    ConditionalWassersteinGANGP,
)
from vegans.models.conditional.ConditionalVanillaVAE import ConditionalVanillaVAE

if __name__ == '__main__':

    loader = loading.CelebALoader(batch_size=16, max_loaded_images=1000, output_shape=64)
    train_dataloader = loader.load()

    epochs = 3

    X_train, y_train = iter(train_dataloader).next()
    x_dim = X_train.numpy().shape[1:]
    y_dim = y_train.numpy().shape[1:]
    z_dim = 128

    ######################################C###################################
    # Architecture
    #########################################################################
    # loader = loading.ExampleLoader()
    generator = loader.load_generator(x_dim=x_dim, z_dim=z_dim, y_dim=y_dim)
    discriminator = loader.load_adversary(x_dim=x_dim, y_dim=y_dim, adv_type="Discriminator")
    critic = loader.load_adversary(x_dim=x_dim, y_dim=y_dim, adv_type="Critic")
    encoder = loader.load_encoder(x_dim=x_dim, z_dim=z_dim, y_dim=y_dim)
    decoder = loader.load_decoder(x_dim=x_dim, z_dim=z_dim, y_dim=y_dim)

    #########################################################################
    # Training
    #########################################################################
    models = [
        #ConditionalBicycleGAN, ConditionalKLGAN
        ConditionalLRGAN, ConditionalLSGAN,
        ConditionalPix2Pix, ConditionalVAEGAN, ConditionalVanillaGAN,
        ConditionalVanillaVAE , ConditionalWassersteinGAN, ConditionalWassersteinGANGP,
        ConditionalWassersteinGAN, ConditionalWassersteinGANGP,
    ]

    for model in models:
        kwargs = {"x_dim": x_dim, "z_dim": z_dim, "y_dim": y_dim}

        if model.__name__ in ["ConditionalAAE"]:
            discriminator_aee = loading.ExampleLoader().load_adversary(x_dim=z_dim, y_dim=y_dim, adv_type="Discriminator")
            gan_model = model(
                generator=generator, adversary=discriminator_aee, encoder=encoder, **kwargs
            )

        elif model.__name__ in ["ConditionalBicycleGAN", "ConditionalVAEGAN"]:
            encoder_reduced = loader.load_encoder(x_dim=x_dim, z_dim=z_dim*2, y_dim=y_dim)
            gan_model = model(
                generator=generator, adversary=discriminator, encoder=encoder_reduced, **kwargs
            )

        elif model.__name__ in ["ConditionalEBGAN"]:
            m = np.mean(X_train)
            gan_model = model(
                generator=generator, adversary=autoencoder, m=m, **kwargs
            )

        elif model.__name__ in ["ConditionalKLGAN", "ConditionalLSGAN", "ConditionalPix2Pix", "ConditionalVanillaGAN"]:
            gan_model = model(
                generator=generator, adversary=discriminator, **kwargs
            )

        elif model.__name__ in ["ConditionalLRGAN"]:
            gan_model = model(
                generator=generator, adversary=discriminator, encoder=encoder, **kwargs
            )

        elif model.__name__ in ["ConditionalVanillaVAE"]:
            encoder_reduced = loader.load_encoder(x_dim=x_dim, z_dim=z_dim*2, y_dim=y_dim)
            gan_model = model(
                encoder=encoder_reduced, decoder=decoder, **kwargs
            )

        elif model.__name__ in ["ConditionalWassersteinGAN", "ConditionalWassersteinGANGP"]:
            gan_model = model(
                generator=generator, adversary=critic, **kwargs
            )

        else:
            raise NotImplementedError("{} no yet implemented in logical gate.".format(model.__name__))

        gan_model.summary(save=True)
        gan_model.fit(
            X_train=train_dataloader,
            y_train=None,
            X_test=None,
            y_test=None,
            batch_size=None,
            epochs=epochs,
            steps=None,
            print_every=500,
            save_model_every=None,
            save_images_every="0.1e",
            save_losses_every=10,
            enable_tensorboard=False
        )
        samples, losses = gan_model.get_training_results(by_epoch=False)

        training_time = np.round(gan_model.total_training_time/60, 2)
        title = "Epochs: {}, z_dim: {}, Time trained: {} minutes\nParams: {}\n\n".format(
            epochs, z_dim, training_time, gan_model.get_number_params()
        )
        fig, axs = utils.plot_images(images=samples, show=False)
        fig.suptitle(title, fontsize=12)
        fig.tight_layout()
        plt.savefig(gan_model.folder+"/generated_images.png")

        fig, axs = utils.plot_losses(losses=losses, show=False)
        fig.suptitle(title, fontsize=12)
        fig.tight_layout()
        plt.savefig(gan_model.folder+"/losses.png")
        # gan_model.save()